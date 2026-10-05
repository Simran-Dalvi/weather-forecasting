import time
import pandas as pd

from weather_forecasting.api.fetch_weather_api import WeatherAPI
from weather_forecasting.config.constants import (
    HISTORY_DAYS,
    LATITUDE,
    LONGITUDE,
)
from weather_forecasting.data.raw_dataset import (
    load_latest_data,
    save_latest_data,
)

from weather_forecasting.utils.logger import logger
from weather_forecasting.config.constants import (
    REQUIRED_COLUMNS,
    FRESHNESS_THRESHOLD_HOURS,
    MAXIMUM_FRESHNESS_RETRY,
    RETRY_DELAYS)


def validate_weather_data(df:pd.DataFrame) -> pd.DataFrame:
    """
    Validate weather data before it is merged with the existing dataset.

    Raises:
        ValueError: If the weather data is invalid.
    """

    if df.empty:
        raise ValueError("Weather API returned empty data.")

    df = df.copy()

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Weather data is missing required columns: {missing_columns}"
        )

    # Convert timestamps to UTC
    df["date"] = pd.to_datetime(
        df["date"],
        utc = True,
        errors="coerce"
    )

    # Check for invalid timestamps
    if df["date"].isna().any():
        raise ValueError(
            "Weather data contains invalid timestamps."
        )

    # Weather columns must be numeric
    weather_columns = REQUIRED_COLUMNS - {"date"}

    for column in weather_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Check for invalid weather values
    if df[list(weather_columns)].isna().any().any():
        raise ValueError(
            "Weather data contains missing or invalid weather values."
        )

    return df

def get_latest_observation_timestamp(
        df: pd.DataFrame,
) -> pd.Timestamp | None:
    """
    Return the latest completed hourly observation timestamp.
    Future forecast timestamps are ignored.
    """

    if df.empty:
        return None

    now = pd.Timestamp.now(tz="UTC")
    current_hour = now.floor("h")

    timestamps = pd.to_datetime(
        df["date"],
        utc=True,
        errors="coerce",
    )

    completed_hours = timestamps[timestamps < current_hour]

    if completed_hours.empty:
        return None

    return completed_hours.max()

def get_data_age(
        df: pd.DataFrame,
) -> pd.Timedelta | None:
    """
    Return the age of the latest completed observation.
    """
    latest_observation = get_latest_observation_timestamp(df)

    if latest_observation is None:
        return None

    now = pd.Timestamp.now(tz="UTC")

    return now - latest_observation

def is_data_stale(
        df: pd.DataFrame,
        threshold_hours: int = FRESHNESS_THRESHOLD_HOURS
) -> bool:
    """
    Determine whether the latest completed observation
    is older than the allowed freshness threshold.
    """

    data_age = get_data_age(df)

    if data_age is None:
        logger.warning("No completed weather observation is available.")
        return True

    threshold = pd.Timedelta(hours = threshold_hours)

    logger.debug(
        f"Latest observation age is: {data_age} | Freshness threshold: {threshold}"
    )

    return data_age > threshold

def find_missing_timestamps(
        df: pd.DataFrame,
) -> pd.DatetimeIndex:
    """
    Find missing hourly timestamps in weather dataset.
    """
    logger.debug("Finding missing completed-hour timestamps.")

    now = pd.Timestamp.now(tz = "UTC")

    timestamps = (
        pd.to_datetime(df["date"], utc = True, errors="coerce")
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    # Ignore the current hour and future forecast hours.
    completed_hours = timestamps[timestamps < now.floor("h")]

    if len(completed_hours) < 2:
        return pd.DatetimeIndex([])

    expected_timestamps = pd.date_range(
        start= completed_hours.min(),
        end= completed_hours.max(),
        freq="1h",
        tz="UTC",
    )

    return expected_timestamps.difference(completed_hours)

def group_missing_timestamps(
        missing_timestamps: pd.DatetimeIndex
)-> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """
    Group consecutive missing hourly timestamps into gaps.

    Example:
        12:00, 13:00, 14:00
        becomes:
        (12:00, 14:00)
    """

    logger.debug(f"There were {len(missing_timestamps)} missing timestamps found.")

    if len(missing_timestamps) == 0:
        return []

    missing_timestamps = missing_timestamps.sort_values()

    gaps = []

    gap_start = missing_timestamps[0]
    previous_timestamp = missing_timestamps[0]

    for timestamp in missing_timestamps[1:]:
        if timestamp-previous_timestamp != pd.Timedelta(hours=1):
            gaps.append(
                (gap_start, previous_timestamp)
            )
            gap_start = timestamp

        previous_timestamp = timestamp

    gaps.append(
        (gap_start, previous_timestamp)
    )

    return gaps

def recover_missing_timestamps(
        df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Recover missing hourly weather timestamps 
    by requesting weather data around each detected gap.
    """
    missing_timestamps = find_missing_timestamps(df)

    if missing_timestamps.empty:
        logger.debug("No missing houlry timestamps")
        return df

    gaps = group_missing_timestamps(missing_timestamps)

    logger.warning(f"Detected {len(gaps)} missing data gap(s).")

    api = WeatherAPI()
    recovered_data = []

    for gap_start, gap_end in gaps:
        fetch_start = gap_start - pd.Timedelta(hours = 1)
        fetch_end = gap_end + pd.Timedelta(hours = 1)

        logger.debug(f"Recovering gap from  range {gap_start} to {gap_end}. Requesting data from {fetch_start.date()} to {fetch_end.date()}")

        new_data = api.fetch_historical_weather(
             latitude= LATITUDE,
            longitude= LONGITUDE,
            start_date= fetch_start.date().isoformat(),
            end_date= fetch_end.date().isoformat(),
        )

        new_data = validate_weather_data(new_data)

        recovered_data.append(new_data)

    if not recovered_data:
        logger.debug("Nothing was fetched during the missing timestamp fetching phase.")
        return df

    recovered_data = pd.concat(
        recovered_data,
        ignore_index=True
    )

    combined_data = pd.concat(
        [df, recovered_data], ignore_index= True,
    )

    combined_data = (
            combined_data
            .drop_duplicates(subset="date", keep="last")
            .sort_values("date")
            .reset_index(drop=True)
        )

    logger.info(
        f"Missing data recovery complete. Total records {len(combined_data)}"
    )

    return combined_data

def retry_latest_weather(
        existing_data: pd.DataFrame,
        retries: int = MAXIMUM_FRESHNESS_RETRY,
        delays: list[int] = RETRY_DELAYS,
    ) -> pd.DataFrame:
    """
    Retry fetching weather data when the dataset is stale.

    Each retry fetches the latest weather data, validate it,
    merges it with the existing data, and check freshness again.

    If the data becomes fresh, return immediately.
    If the data remains stale after all retries, return the 
    latest valid data with a warning.
    """

    logger.info("Inside the freshness retry loop.")

    if len(delays) < retries:
        raise ValueError("Not enough retry delays configured.")

    api = WeatherAPI()

    combined_data = existing_data.copy()

    for attempt in range(retries):
        delay = delays[attempt]

        if delay > 0:
            logger.info(f"Waiting {delay} minutes before freshness retry.")
            time.sleep(delay * 60)

        logger.debug(f"Freshness retry attempt {attempt + 1}/{retries}")

        # Fetch latest weather
        new_data = api.fetch_latest_weather(
            latitude = LATITUDE,
            longitude=LONGITUDE,
        )

        # Validate incoming data
        new_data = validate_weather_data(new_data)

        # Merge with existing data
        combined_data = pd.concat(
            [combined_data, new_data],
            ignore_index = True,
        )

        combined_data = (
            combined_data
            .drop_duplicates(subset="date", keep="last")
            .sort_values("date")
            .reset_index(drop=True)
        )

        # Check freshness
        if not is_data_stale(combined_data):
            logger.info(f"Weather data became fresh on retry attempt {attempt + 1}.")
            return combined_data

        logger.warning(f"Weather data is still stale after attempt {attempt + 1}")

    logger.warning(f"Weather data is still stale after all {retries} retry attempts.")

    return combined_data



def ingest_weather_data() -> pd.DataFrame:
    """
    Fetch new weather data, merge it with existing raw data,
    remove duplicate timestamps, and retain the required historical window.
    """

    logger.info("Starting weather data ingestion.")

    # Load existing raw data if it exists
    try:
        existing_data = load_latest_data()
    except FileNotFoundError:
        existing_data = pd.DataFrame() #initalize a df

    if existing_data.empty:
        logger.debug("No existing weather data found.")
    else:
        existing_data["date"] = pd.to_datetime(
            existing_data["date"],
            utc=True,
        )

        logger.debug(
            "Loaded existing weather data: %d rows, latest date: %s",
            len(existing_data),
            existing_data["date"].max(),
        )

    api = WeatherAPI()

    new_data = api.fetch_latest_weather(
        latitude= LATITUDE,
        longitude= LONGITUDE,
        past_days = 2,
        forecast_days = 2,
    )

    logger.debug(
        "Fetched %d recent/forecast weather records.",
        len(new_data),
    )

    new_data = validate_weather_data(new_data)

    # Merge existing and new data
    combined_data = pd.concat(
        [existing_data, new_data],
        ignore_index = True,
    )

    # Remove duplicate hourly timestamps
    combined_data = (
        combined_data
        .drop_duplicates(subset="date", keep="last")
        .sort_values("date")
        .reset_index(drop=True)
    )

    logger.debug(
        "After duplicate handling: %d records.",
        len(combined_data),
    )

    # Recover missing timestamps
    combined_data = recover_missing_timestamps(combined_data)

    logger.debug(f"Recovered missing data if present. Total records: {len(combined_data)}")

    # Check for stale data
    if is_data_stale(combined_data):
        logger.warning("Weather data is stale after ingestion. Starting freshness retries.")
        combined_data = retry_latest_weather(existing_data=combined_data,)
    else:
        logger.info("Weather data freshness check passed.")

    # Retain one year of historical data
    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=HISTORY_DAYS)

    combined_data = combined_data[
        combined_data["date"] >= cutoff
    ].copy()

    # Save updated raw data
    save_latest_data(combined_data)

    logger.info(
        f"Weather ingestion completed: {len(combined_data)} rows stored."
    )

    return combined_data


if __name__ == "__main__":
    ingest_weather_data()
