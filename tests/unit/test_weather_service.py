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
    from datetime import datetime, timezone

    import weather_forecasting.server.services.weather as weather_module

    saved_prediction = {
        "prediction_time": datetime(
            2026, 9, 12, 11, 0, tzinfo=timezone.utc
        ),
        "target_time": datetime(
            2026, 9, 12, 11, 0, tzinfo=timezone.utc
        ),
        "temperature_1hr_prediction": 26.5,
    }

    def fake_load_latest_prediction():
        return saved_prediction

    monkeypatch.setattr(
        weather_module,
        "load_latest_prediction",
        fake_load_latest_prediction,
    )

    service = weather_module.WeatherService()

    result = service.predict_next_hour()

    assert result.generated_at == saved_prediction["prediction_time"]
    assert result.predictions[0].target_time == saved_prediction["target_time"]
    assert result.predictions[0].predictions.temperature == 26.5