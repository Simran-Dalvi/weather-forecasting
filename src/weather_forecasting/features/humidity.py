"""
Humidity-specific feature builders.

This module defines humidity-related features while delegating
the underlying feature calculations to BaseFeature.
"""

import pandas as pd

from weather_forecasting.features.base import BaseFeature
from weather_forecasting.config.constants import HUMIDITY_COL


def add_humidity_lags(
        df: pd.DataFrame,
        lags: list[int],
) -> pd.DataFrame:
    """
    Add lag features for humidity
    """
    return BaseFeature.add_lag_features(
        df = df,
        column=HUMIDITY_COL,
        lags = lags,
    )

def add_humidity_rolling_mean(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling mean features for humidity
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column=HUMIDITY_COL,
        windows=windows,
        statistic = "mean"
    )

def add_humidity_rolling_std(
        df: pd.DataFrame,
        windows: list[int],
) -> pd.DataFrame:
    """
    Add rolling std features for humidity
    """
    return BaseFeature.add_rolling_features(
        df = df,
        column=HUMIDITY_COL,
        windows=windows,
        statistic = "std"
    )

def add_humidity_changes(
        df: pd.DataFrame,
        periods: list[int],
) -> pd.DataFrame:
    """
    Add humidity change features.
    Example:
        humidity_change_1
        humidity_change_3
        humidity_change_24
    """
    return BaseFeature.add_change_features(
        df,
        column = HUMIDITY_COL,
        changes = periods,
    )