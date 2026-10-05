"""
Temperature-specific feature builders.

This module defines temperature-related features while delegating
the underlying feature calculations to BaseFeature.
"""

import pandas as pd

from weather_forecasting.config.constants import TEMPERATURE_COL
from weather_forecasting.features.base import BaseFeature

def add_temperature_lags(
        df: pd.DataFrame,
        lags: list[int],
) -> pd.DataFrame:
    """
    Add lag features for temperature
    """
    return BaseFeature.add_lag_features(
        df = df,
        column = TEMPERATURE_COL,
        lags = lags,
    )

def add_temperature_rolling_mean(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling mean features for temperature.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = TEMPERATURE_COL,
        windows = windows,
        statistic = "mean",
    )

def add_temperature_rolling_std(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling std features for temperature.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = TEMPERATURE_COL,
        windows = windows,
        statistic = "std",
    )

def add_temperature_changes(
        df : pd.DataFrame,
        periods: list[int],
)-> pd.DataFrame:
    """
    Add temperature change features.
    Example:
        temp_change_1
        temp_change_3
        temp_change_24
    """
    return BaseFeature.add_change_features(
        df,
        column= TEMPERATURE_COL,
        changes= periods)