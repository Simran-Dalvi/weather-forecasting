"""
Wind-specific feature builders.

This module defines wind-related features while delegating
the underlying feature calculations to BaseFeature.
"""

import pandas as pd
from weather_forecasting.config.constants import WIND_COL
from weather_forecasting.features.base import BaseFeature

def add_wind_lags(
        df: pd.DataFrame,
        lags: list[int],
) -> pd.DataFrame:
    """
    Add lag features for wind
    """
    return BaseFeature.add_lag_features(
        df = df,
        column=WIND_COL,
        lags=lags,
    )

def add_wind_rolling_mean(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling mean features for wind.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column=WIND_COL,
        windows=windows,
        statistic="mean",
    )

def add_wind_rolling_std(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling std features for wind.
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column = WIND_COL,
        windows= windows,
        statistic="std",
    )

def add_wind_changes(
        df: pd.DataFrame,
        periods : list[int],
) -> pd.DataFrame:
    """
    Add wind change features.
    Example:
        wind_change_1
        wind_change_3
        wind_Change_24
    """
    return BaseFeature.add_change_features(
        df,
        column=WIND_COL,
        changes=periods,
    )