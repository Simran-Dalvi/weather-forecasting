"""
Fetch weather data from the Open-Meteo API
"""

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


class WeatherAPI:
    """
    Handles communication with Open-Meteo API
    """

    def __init__(self):
        cache_session = requests_cache.CachedSession(".cache", expire_after=600)

        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        self.client = openmeteo_requests.Client(session=retry_session)

    def fetch_historical_weather(
        self, latitude: float, longitude: float, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        Fetch historical hourly weather data,

        Parameters
        ----------
        latitude : float
        longitude : float
        start_date : str (YYYY-MM-DD)
        end_date : str (YYYY-MM-DD)

        Returns
        --------
        pd.DataFrame
        """

        url = "https://archive-api.open-meteo.com/v1/archive"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "rain",
                "wind_speed_10m",
                "soil_temperature_0_to_7cm",
                "soil_moisture_0_to_7cm",
                "surface_pressure",
            ],
        }
        responses = self.client.weather_api(url, params=params)

        response = responses[0]
        hourly = response.Hourly()

        data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            ),
            "Temperature": hourly.Variables(0).ValuesAsNumpy(),
            "Humidity": hourly.Variables(1).ValuesAsNumpy(),
            "Rain": hourly.Variables(2).ValuesAsNumpy(),
            "Wind_Speed": hourly.Variables(3).ValuesAsNumpy(),
            "Soil_Temp": hourly.Variables(4).ValuesAsNumpy(),
            "Soil_Moisture": hourly.Variables(5).ValuesAsNumpy(),
            "Pressure": hourly.Variables(6).ValuesAsNumpy(),
        }

        return pd.DataFrame(data)

    def fetch_latest_weather(
        self,
        latitude: float,
        longitude: float,
        past_days: int = 2,
        forecast_days: int = 2,
        ) -> pd.DataFrame:
        """
        Fetch recent, current, and forecast hourly weather data.

        Parameters
        -----------
        latitude: float
            Location latitude
        longitude: float
            Location longitude
        past_days: int, default = 2
            Number of recent past days to request.
        forecast_days: int, default=2
            Number of future forecast days to request.

        Returns
        -------
        pd.DataFrame
            Hourly weather data including recent observations
            and future forecast rows.
        """

        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": forecast_days,
            "past_days": past_days,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "rain",
                "wind_speed_10m",
                "soil_temperature_0_to_7cm",
                "soil_moisture_0_to_7cm",
                "surface_pressure",
            ],
        }

        responses = self.client.weather_api(url, params=params)

        response = responses[0]
        hourly = response.Hourly()

        data = {
            "date": pd.date_range(
                start = pd.to_datetime(
                    hourly.Time(),
                    unit = "s",
                    utc=True,
                ),
            end = pd.to_datetime(
                hourly.TimeEnd(),
                unit = "s",
                utc = True,
            ),
            freq = pd.Timedelta(seconds=hourly.Interval()),
            inclusive = "left",
            ),
            "Temperature": hourly.Variables(0).ValuesAsNumpy(),
            "Humidity": hourly.Variables(1).ValuesAsNumpy(),
            "Rain": hourly.Variables(2).ValuesAsNumpy(),
            "Wind_Speed": hourly.Variables(3).ValuesAsNumpy(),
            "Soil_Temp": hourly.Variables(4).ValuesAsNumpy(),
            "Soil_Moisture": hourly.Variables(5).ValuesAsNumpy(),
            "Pressure": hourly.Variables(6).ValuesAsNumpy(),
        }

        return pd.DataFrame(data)   