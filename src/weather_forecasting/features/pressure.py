"""
Pressure-specific feature builders.

This module defines pressure-related features while delegating
the underlying feature calculations to BaseFeature.
"""

import pandas as pd

from weather_forecasting.config.constants import PRESSURE_COL
from weather_forecasting.features.base import BaseFeature

def add_pressure_lags(
        df: pd.DataFrame,
        lags: list[int],
) -> pd.DataFrame:
    """
    Add lag features for pressure.
    """
    return BaseFeature.add_lag_features(
        df= df,
        column=PRESSURE_COL,
        lags=lags,
    )

def add_pressure_rolling_mean(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling mean features for pressure.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = PRESSURE_COL,
        windows = windows,
        statistic = "mean",
    )

def add_pressure_rolling_std(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling std features for pressure.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = PRESSURE_COL,
        windows = windows,
        statistic = "std",
    )

def add_pressure_changes(
        df : pd.DataFrame,
        periods: list[int],
) -> pd.DataFrame:
    """
    Add pressure change features.
    Example:
        pressure_change_1
        pressure_change_3
        pressure_change_24
    """
    return BaseFeature.add_change_features(
        df,
        column= PRESSURE_COL,
        changes= periods)