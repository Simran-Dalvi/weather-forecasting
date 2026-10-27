from weather_forecasting.config.constants import LOCATION
from weather_forecasting.data.raw_dataset import load_today_data
from weather_forecasting.server.schemas.weather import (
    Location, WeatherPrediction, WeatherPredictionPoint,
    WeatherPredictionResponse,WeatherObservation, CurrentWeatherResponse)
from weather_forecasting.data.prediction_dataset import load_latest_prediction
from weather_forecasting.server.exceptions import (WeatherDataNotFoundError, 
                                                   PredictionError,
                                                   PredictionUnavailableError,
                                                   )
from weather_forecasting.utils.logger import logger


class WeatherService:
    """Business logic for weather operations."""

    def predict_next_hour(self) -> WeatherPredictionResponse:
        """
        Return the latest saved next-hour temperature prediction.
        """
        logger.info("Loading the latest saved weather prediction.")

        try:
            prediction_result = load_latest_prediction()
        except (FileNotFoundError, ValueError) as exc:
            logger.error(f"Failed to load a usable saved prediction: {exc}")
            raise PredictionUnavailableError(str(exc)) from exc

        prediction_time = prediction_result["prediction_time"]
        target_time = prediction_result["target_time"]
        predicted_temperature = prediction_result["temperature_1hr_prediction"]

        return WeatherPredictionResponse(
            generated_at=prediction_time,
            location=Location(**LOCATION),
            predictions = [
                WeatherPredictionPoint(
                    target_time=target_time,
                    predictions = WeatherPrediction(
                        temperature=float(predicted_temperature),
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