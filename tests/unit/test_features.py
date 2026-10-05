import numpy as np
import pandas as pd
import pytest

from weather_forecasting.features.base import BaseFeature
from weather_forecasting.features.time import add_time_features
from weather_forecasting.features.temperature import(
    add_temperature_lags,
    add_temperature_changes,
)

def test_add_lag_features():
    df = pd.DataFrame({
        "Temperature": [20, 21, 22, 23, 24],
    })

    result = BaseFeature.add_lag_features(
        df,
        column = "Temperature",
        lags = [1],
    )

    assert "Temperature_lag_1" in result.columns
    assert pd.isna(result.loc[0, "Temperature_lag_1"])
    assert result.loc[1, "Temperature_lag_1"] == 20
    assert result.loc[4, "Temperature_lag_1"] == 23

def test_add_change_features():
    df = pd.DataFrame({
        "Temperature": [20, 21, 23, 22],
    })

    result = BaseFeature.add_change_features(
        df,
        column = "Temperature",
        changes = [1],
    )

    assert "Temperature_change_1" in result.columns
    assert pd.isna(result.loc[0, "Temperature_change_1"])
    assert result.loc[1, "Temperature_change_1"] == 1
    assert result.loc[2, "Temperature_change_1"] == 2
    assert result.loc[3, "Temperature_change_1"] == -1

def test_add_rolling_mean():
    df = pd.DataFrame({
        "Temperature": [10, 20, 30, 40],
    })

    result = BaseFeature.add_rolling_features(
        df,
        column = "Temperature",
        windows = [2],
        statistic = "mean",
    )

    assert "Temperature_rolling_mean_2" in result.columns
    assert pd.isna(result.loc[0, "Temperature_rolling_mean_2"])
    assert result.loc[1, "Temperature_rolling_mean_2"] == 15
    assert result.loc[2, "Temperature_rolling_mean_2"] == 25
    assert result.loc[3, "Temperature_rolling_mean_2"] == 35

def test_add_rolling_std():
    df = pd.DataFrame({
        "Temperature": [10, 20, 30],
    })

    result = BaseFeature.add_rolling_features(
        df,
        column = "Temperature",
        windows = [2],
        statistic="std",
    )

    assert "Temperature_rolling_std_2" in result.columns

    expected = np.std([10, 20], ddof=1)

    assert pd.isna(result.loc[0, "Temperature_rolling_std_2"])
    assert result.loc[1, "Temperature_rolling_std_2"] == expected


def test_create_target():
    df = pd.DataFrame({
        "Temperature": [20, 21, 22, 23],
    })

    result = BaseFeature.create_target(
        df,
        column = "Temperature",
        horizon=1,
    )

    assert "target_Temperature_1" in result.columns
    assert result.loc[0, "target_Temperature_1"] == 21
    assert result.loc[1, "target_Temperature_1"] == 22
    assert pd.isna(result.loc[3, "target_Temperature_1"])

def test_missing_column_raises_error():
    df = pd.DataFrame({
        "Humidity": [50, 60, 70],
    })

    with pytest.raises(KeyError):
        BaseFeature.add_lag_features(
            df,
            column = "Temperature",
            lags = [1],
        )

def test_invalid_lag_raises_error():
    df = pd.DataFrame({
        "Temperature": [20, 21, 22],
    })

    with pytest.raises(ValueError):
        BaseFeature.add_lag_features(
            df,
            column = "Temperature",
            lags = [0],
        )

def test_invalid_rolling_statistic_raises_error():
    df = pd.DataFrame({
        "Temperature": [20, 21, 22],
    })

    with pytest.raises(ValueError):
        BaseFeature.add_rolling_features(
            df,
            column ="Temperature",
            windows = [2],
            statistic = "median",
        )

def test_invalid_target_horizon_raises_error():
    df = pd.DataFrame({
        "Temperature": [20, 21, 22],
    })

    with pytest.raises(ValueError):
        BaseFeature.create_target(
            df,
            column = "Temperature",
            horizon = 0,
        )

def test_time_features():
    df = pd.DataFrame({
        "date": [
            "2026-09-10 06:00:00",
            "2026-09-10 12:00:00",
        ]
    })

    result = add_time_features(df)

    assert result.loc[0, "hour"] == 6
    assert result.loc[0, "day"] == 10
    assert result.loc[0, "month"] == 9

    assert result.loc[1, "hour"] == 12

    assert np.isclose(result.loc[0, "hour_sin"], 1.0, atol=1e-10)
    assert np.isclose(result.loc[1, "hour_cos"], -1.0, atol = 1e-10)

def test_temperature_lag_wrrapper():
    df = pd.DataFrame({
        "Temperature": [20, 21, 22],
    })

    result = add_temperature_lags(
        df,
        lags = [1],
    )

    assert "Temperature_lag_1" in result.columns
    assert result.loc[1, "Temperature_lag_1"] == 20

def test_temperature_change_wrapper():
    df = pd.DataFrame({
        "Temperature": [20, 22, 21],
    })

    result = add_temperature_changes(
        df,
        periods = [1],
    )

    assert "Temperature_change_1" in result.columns
    assert result.loc[1, "Temperature_change_1"] == 2
    assert result.loc[2, "Temperature_change_1"] == -1