from pathlib import Path
import pandas as pd
from weather_forecasting.config.paths import DATA_DIR


RAW_DATA_DIR = DATA_DIR / "raw"


def save_latest_data(df: pd.DataFrame, filename: str = "latest_weather.csv") -> Path:
    """
    Overwrite the latest weather data.
    Used for inference
    """
    file_path = RAW_DATA_DIR / filename
    df.to_csv(file_path, index=False)
    
    return file_path


def update_weather_history(
    df: pd.DataFrame,
    filename: str = "weather_history.csv",
) -> Path:
    """
    Append only new rows to the historical dataset.
    """
    history_path = RAW_DATA_DIR / filename

    if history_path.exists():
        history = pd.read_csv(
            history_path,
            parse_dates=["date"],
        )

        df["date"] = pd.to_datetime(df["date"])

        history["date"] = pd.to_datetime(history["date"])

        combined = pd.concat([history, df], ignore_index=True)

        combined = (
            combined.drop_duplicates(subset="date")
            .sort_values("date")
            .reset_index(drop=True)
        )

    else:
        combined = df.copy()

    combined.to_csv(history_path, index=False)

    return history_path

def load_latest_data(filename: str = "latest_weather.csv") -> pd.DataFrame:
    """
    Load the latest raw weather dataset.

    Raises:
        FileNotFound Error if the dataset does not exist.
    """
    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: (file_path) \n"
            "Run the weather fetching pipeline first."
        )
    
    return pd.read_csv(file_path)

def load_today_data(
        filename: str = "latest_weather.csv",
) -> pd.DataFrame:
    """
    Load today's hourly weather data from the latest raw dataset.

    Returns:
        DataFrame contaning only today's weather observations.
    """
    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found:{file_path}."
            "Run the weather fetching pipeline first."
        )

    df = pd.read_csv(
        file_path,
        parse_dates = ["date"],
    )

    df["date"] = pd.to_datetime(df["date"], utc=True)

    local_dates = df["date"].dt.tz_convert("Asia/Kolkata")

    today = pd.Timestamp.now(tz="Asia/Kolkata").date()

    today_data = df[
        local_dates.dt.date == today
    ].copy()

    return today_data

