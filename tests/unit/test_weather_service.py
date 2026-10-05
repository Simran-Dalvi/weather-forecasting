from datetime import datetime

import pandas as pd
import pytest

from weather_forecasting.server.exceptions import WeatherDataNotFoundError
from weather_forecasting.server.services.weather import WeatherService


def test_get_current_weather(monkeypatch):
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2026-09-12 06:00:00+00:00",
                    "2026-09-12 07:00:00+00:00",
                ]
            ),
            "Temperature": [24.5, 25.0],
            "Humidity": [75.0, 72.0],
            "Rain": [0.0, 0.1],
            "Wind_Speed": [10.0, 12.0],
            "Soil_Temp": [23.0, 23.5],
            "Soil_Moisture": [0.4, 0.42],
            "Pressure": [1005.0, 1006.0],
        }
    )

    monkeypatch.setattr(
        "weather_forecasting.server.services.weather.load_today_data",
        lambda: df,
    )

    service = WeatherService()

    result = service.get_current_weather()

    assert result.source == "Open-Meteo API"
    assert result.location.name == "Pune"
    assert len(result.hourly) == 2

    assert result.hourly[0].temperature == 24.5
    assert result.hourly[0].humidity == 75.0
    assert result.hourly[1].temperature == 25.0


def test_get_current_weather_no_data(monkeypatch):
    empty_df = pd.DataFrame()

    monkeypatch.setattr(
        "weather_forecasting.server.services.weather.load_today_data",
        lambda: empty_df,
    )

    service = WeatherService()

    with pytest.raises(WeatherDataNotFoundError):
        service.get_current_weather()


def test_predict_next_hour(monkeypatch):
    class FakePredictor:
        def predict(self):
            return {
                "input_time": "2026-09-12T10:00:00+00:00",
                "prediction": 26.5,
            }

    service = WeatherService()

    result = service.predict_next_hour(FakePredictor())

    assert result.location.name == "Pune"
    assert len(result.predictions) == 1

    prediction = result.predictions[0]

    assert prediction.target_time == datetime.fromisoformat(
        "2026-09-12T11:00:00+00:00"
    )

    assert prediction.predictions.temperature == 26.5