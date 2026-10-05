"""
Soil-temperature-specific feature builders.

This module defines soil temperature-related features while delegating
the underlying feature calculations to BaseFeature.
"""

import pandas as pd

from weather_forecasting.config.constants import SOIL_TEMPERATURE_COL
from weather_forecasting.features.base import BaseFeature

def add_soil_temp_lags(
        df: pd.DataFrame,
        lags: list[int],
) -> pd.DataFrame:
    """
    Add lag features for soil temperature.
    """
    return BaseFeature.add_lag_features(
        df = df,
        column = SOIL_TEMPERATURE_COL,
        lags = lags,
    )

def add_soil_temp_rolling_mean(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling mean features for soil temperature.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = SOIL_TEMPERATURE_COL,
        windows = windows,
        statistic = "mean",
    )

def add_soil_temp_rolling_std(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling std features for soil temperature.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = SOIL_TEMPERATURE_COL,
        windows = windows,
        statistic = "std",
    )

def add_soil_temp_changes(
        df: pd.DataFrame,
        periods: list[int],
) -> pd.DataFrame:
    """
    Add soil temperature change features.
    Example:
        temp_change_1
        temp_change_3
        temp_change_24
    """
    return BaseFeature.add_change_features(
        df,
        column= SOIL_TEMPERATURE_COL,
        changes= periods)