from datetime import datetime, timedelta, timezone

from weather_forecasting.config.constants import LOCATION
from weather_forecasting.data.raw_dataset import load_today_data
from weather_forecasting.inference.predictor import Predictor
from weather_forecasting.server.schemas.weather import (
    Location, WeatherPrediction, WeatherPredictionPoint,
    WeatherPredictionResponse,WeatherObservation, CurrentWeatherResponse)

from weather_forecasting.server.exceptions import WeatherDataNotFoundError
from weather_forecasting.utils.logger import logger


class WeatherService:
    """Business logic for weather operations."""

    def predict_next_hour(self, predictor: Predictor) -> WeatherPredictionResponse:
        """Generate the next-hour weather prediction."""

        logger.info("Generating next-hour weather prediction.")

        prediction_result = predictor.predict()

        input_time = datetime.fromisoformat(prediction_result["input_time"])

        target_time = input_time + timedelta(hours=1)

        return WeatherPredictionResponse(
            generated_at=datetime.now(timezone.utc),
            location=Location(**LOCATION),
            predictions=[
                WeatherPredictionPoint(
                    target_time=target_time,
                    predictions=WeatherPrediction(
                        temperature=prediction_result["prediction"],
                    ),
                )
            ],
        )

    def get_current_weather(self) -> CurrentWeatherResponse:
        """Returns today's hourly weather observations."""

        logger.info("Loading today's weather data.")

        df = load_today_data()

        if df.empty:
            logger.warning("No weather data available for today.")

            raise WeatherDataNotFoundError(
                "No weather data available for today."
            )
        
        hourly = [
            WeatherObservation(
                timestamp= row.date,
                temperature=row.Temperature,
                humidity = row.Humidity,
                rain = row.Rain,
                wind_speed= row.Wind_Speed,
                soil_temperature= row.Soil_Temp,
                soil_moisture= row.Soil_Moisture,
                pressure= row.Pressure,
            )
            for row in df.itertuples(index=False)
        ]

        logger.info(f"Data Loaded successfully: {len(df)}")

        return CurrentWeatherResponse(
            source= "Open-Meteo API",
            location= Location(**LOCATION),
            hourly= hourly
        )