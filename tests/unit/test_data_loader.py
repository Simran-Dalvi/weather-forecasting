import pandas as pd
import pytest
from datetime import datetime, timezone

today = datetime.now(timezone.utc).date()

from weather_forecasting.data.raw_dataset import (
    load_latest_data,
    load_today_data,
)

from weather_forecasting.data.processed_dataset import (
    load_processed_dataset,
)

def test_load_latest_data(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "weather_forecasting.data.raw_dataset.RAW_DATA_DIR",
        tmp_path,
    )
    file_path = tmp_path / "latest_weather.csv"

    df = pd.DataFrame(
        {
            "date": ["2026-09-10 10:00:00"],
            "Temperature": [25.5],
            "Humidity": [70.0],
        }
    )

    df.to_csv(file_path, index = False)

    result = load_latest_data(filename = str(file_path))

    assert not result.empty

    assert "Temperature" in result.columns
    assert "Humidity" in result.columns


def test_load_latest_data_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_latest_data(filename = str(missing_file))

def test_load_today_data(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "weather_forecasting.data.raw_dataset.RAW_DATA_DIR",
        tmp_path,
    )
    file_path = tmp_path / "latest_weather.csv"

    df = pd.DataFrame(
        {
            "date": [
                f"{today} 05:00:00+00:00",
                f"{today} 06:00:00+00:00",
            ],
            "Temperature": [25.5, 26.0],
            "Humidity": [70.0, 68.0],
        }
    )

    df.to_csv(file_path, index=False)

    result = load_today_data(filename=str(file_path))

    assert not result.empty
    assert len(result) == 2
    assert "Temperature" in result.columns


def test_load_today_data_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_today_data(filename=str(missing_file))


def test_load_processed_dataset(tmp_path):
    file_path = tmp_path / "processed.csv"

    df = pd.DataFrame(
        {
            "date": ["2026-09-10 10:00:00"],
            "Temperature": [25.5],
            "Temperature_lag_1": [25.0],
        }
    )

    df.to_csv(file_path, index=False)

    result = load_processed_dataset(feature_store_path=file_path)

    assert not result.empty
    assert "Temperature" in result.columns
    assert "Temperature_lag_1" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_load_processed_dataset_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_processed_dataset(feature_store_path=missing_file)