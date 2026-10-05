import pytest

from weather_forecasting.api.fetch_weather_api import WeatherAPI


@pytest.fixture(scope="module")
def weather_df():
    api = WeatherAPI()

    return api.fetch_historical_weather(
        latitude=18.5196,
        longitude=73.8554,
        start_date="2025-01-01",
        end_date="2025-01-07",
    )


def test_dataframe_not_empty(weather_df):
    assert not weather_df.empty


def test_expected_columns(weather_df):
    expected = {
        "date",
        "Temperature",
        "Humidity",
        "Pressure",
        "Rain",
        "Soil_Moisture",
        "Soil_Temp",
        "Wind_Speed",
    }

    assert expected.issubset(weather_df.columns)


def test_dates_sorted(weather_df):
    assert weather_df["date"].is_monotonic_increasing


def test_dates_unique(weather_df):
    assert weather_df["date"].is_unique


def test_temperature_not_null(weather_df):
    assert weather_df["Temperature"].notna().all()

