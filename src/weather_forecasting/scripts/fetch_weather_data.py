from datetime import date, timedelta

from weather_forecasting.api.fetch_weather_api import WeatherAPI
from weather_forecasting.config.constants import LATITUDE, LONGITUDE, HISTORY_DAYS
from weather_forecasting.data.raw_dataset import save_latest_data
from weather_forecasting.utils.logger import logger


def fetch_weather_data():
    # end_date = date.today()
    end_date = date(2026, 9, 15)

    start_date = end_date - timedelta(days=HISTORY_DAYS)

    api = WeatherAPI()
    df = api.fetch_historical_weather(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
    )
    save_latest_data(df)

    logger.info("Weather data fetched and stored successfully!")


if __name__ == "__main__":
    fetch_weather_data()
