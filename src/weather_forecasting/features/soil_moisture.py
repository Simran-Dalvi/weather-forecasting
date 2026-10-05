"""
Soil-moisture-specific feature builders.

This module defines soil moisture-related features while delegating
the underlying feature calculations to BaseFeature.
"""

import pandas as pd

from weather_forecasting.config.constants import SOIL_MOISTURE_COL
from weather_forecasting.features.base import BaseFeature

def add_soil_moist_lags(
        df: pd.DataFrame,
        lags: list[int],
) -> pd.DataFrame:
    """
    Add lag features for soil moisture.
    """
    return BaseFeature.add_lag_features(
        df = df,
        column = SOIL_MOISTURE_COL,
        lags = lags,
    )

def add_soil_moist_rolling_mean(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling mean features for soil moisture.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = SOIL_MOISTURE_COL,
        windows = windows,
        statistic = "mean",
    )

def add_soil_moist_rolling_std(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling std features for soil moisture.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = SOIL_MOISTURE_COL,
        windows = windows,
        statistic = "std",
    )

def add_soil_moist_changes(
        df : pd.DataFrame,
        periods: list[int],
) -> pd.DataFrame:
    """
    Add soil moisture change features.
    Example:
        temp_change_1
        temp_change_3
        temp_change_24
    """
    return BaseFeature.add_change_features(
        df,
        column= SOIL_MOISTURE_COL,
        changes= periods)