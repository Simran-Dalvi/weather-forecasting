import pandas as pd
import numpy as np
from weather_forecasting.utils.logger import logger


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract datetime-based features.
    Adds:
    -hour
    -day
    -month
    -hour_sin
    -hour_cos
    -month_sin
    -month_cos
    """

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    df["hour"] = df["date"].dt.hour
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    logger.info("Created cyclical hour features")

    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    logger.info("Created cyclical month features")
    
    return df
