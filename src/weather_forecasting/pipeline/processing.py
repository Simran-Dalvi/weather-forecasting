import pandas as pd
from weather_forecasting.utils.logger import logger
from weather_forecasting.data.raw_dataset import load_latest_data
from weather_forecasting.data.processed_dataset import save_processed_data
from weather_forecasting.features.feature_pipeline.temperature_1hr import build_temperature_1hr_features
from weather_forecasting.config.constants import REQUIRED_COLUMNS
from weather_forecasting.pipeline.ingestion import ingest_weather_data

def validate_raw_data(df: pd.DataFrame) -> None:
    """
    Validate the raw dataset before processing
    """

    if df is None:
        raise ValueError("Raw dataset is None.")

    if df.empty:
        raise ValueError("Raw dataset is empty.")

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Raw dataset is missing required columns: {sorted(missing_columns)}"
        )

    if df["date"].isna().any():
        raise ValueError("Raw dataset contains missing date values.")

    if df["date"].duplicated().any():
        duplicated_count = df["date"].duplicated().sum()

        raise ValueError(
            f"Raw dataset contains {duplicated_count} duplicate timestamps."
        )

def prepare_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize timestamps and prepare the raw dataset for feature engineering.
    """
    df = df.copy()

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], utc=True)

    # Sort chronologically
    df= df.sort_values("date").reset_index(drop=True)

    return df

def restrict_to_current_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep observations up to and including the current hour.

    The current hour is allowed because its weather information
    is used to predict the following hour.
    """

    now = pd.Timestamp.now(tz="UTC")
    current_hour = now.floor("h")

    df = df[df["date"] <= current_hour].copy()

    if df.empty:
        raise ValueError(
            "No completed weather observations are available for processing."
        )

    return df.reset_index(drop=True)

def validate_processed_data(df: pd.DataFrame) -> None:
    """
    Validate the final processed dataset before saving it.
    """
    if df is None:
        raise ValueError("Processed dataset is None.")

    if df.empty:
        raise ValueError("Processed dataset is empty.")

    if "date" not in df.columns:
        raise ValueError("Processed dataset is missing the date column.")

    if df["date"].isna().any():
        raise ValueError("Processed dataset contains missing dates.")

    if df["date"].duplicated().any():
        duplicate_count = df["date"].duplicated().sum()

        raise ValueError(
            f"Processed dataset contains {duplicate_count} duplicate timestamps."
        )

    if not df["date"].is_monotonic_increasing:
        raise ValueError(
            "Processed dataset is not sorted chronologically."
        )

def processing() -> pd.DataFrame:
    """
    Main weather data processing piepline.

    Flow:
        1. Load raw data
        2. Validate raw data
        3. Prepare raw data
        4. Remove future observations
        5. Build model features
        6. Merge raw + engineered features
        7. Validate processed data
        8. Save processed data
        9. Return processed dataframe
    """ 

    logger.info("Starting weather data processing pipeline.")

    try:
        # Load raw data
        logger.info("Loading raw weather dataset.")

        raw_df = load_latest_data()

        logger.info(f"Loaded raw dataset with {len(raw_df)} rows.")

        # Validate raw data
        logger.info("Validate raw dataset.")

        validate_raw_data(raw_df)

        # Prepare raw data
        logger.info("Prepare raw dataset.")

        raw_df = prepare_raw_data(raw_df)

        # Keep observation up to the current hour
        rows_before_filter = len(raw_df)

        raw_df = restrict_to_current_data(raw_df)

        rows_after_filter = len(raw_df)

        logger.info(f"Remove {rows_before_filter - rows_after_filter} future rows.")

        # Build model features
        logger.info("Building temperature 1- hour prediction features.")

        feature_df = build_temperature_1hr_features(raw_df)

        logger.info(f"Generated {len(feature_df.columns) - 1} engineered features.")

        # Validate feature output
        if feature_df.empty:
            raise ValueError(
                "Feature piepline returned an empty dataset."
            )

        if feature_df["date"].duplicated().any():
            raise ValueError(
                "Feature piepline returned duplicate timestamps."
            )

        # Combine raw data + engineered features
        logger.info("Combining raw data with engineered features.")

        feature_columns = [ 
            column
            for column in feature_df.columns
            if column != "date"
            ]

        # #Make sure feature names don't overlap overwrite raw columns.
        overlapping_columns = (
            set(feature_columns) & set(raw_df.columns)
        )

        if overlapping_columns:
            raise ValueError(
                "Feature columns overlap with raw columns:"
                f"{sorted(overlapping_columns)}"
            )

        processed_df = raw_df.merge(
            feature_df,
            on="date",
            how="inner",
            validate="one_to_one",
        )

        # # Always keep chronological ordering
        processed_df = (
            processed_df.sort_values("date")
            .reset_index(drop=True)
        )

        # Validate processed dataset
        logger.info("Validating processed dataset.")

        validate_processed_data(processed_df)

        # Save processed dataset
        logger.info(
            f"Save processed dataset with {len(processed_df)} rows and {len(processed_df.columns)} columns."
        )

        save_processed_data(processed_df)

        logger.info("Weather data rocessing piepline completed successfully.")

        return processed_df
    
    except Exception:
        logger.exception("Weather data processing piepline failed.")
        raise

if __name__ == "__main__":
    ingest_weather_data()
    processing()