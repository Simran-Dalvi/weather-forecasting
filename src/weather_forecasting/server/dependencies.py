from weather_forecasting.config.settings import settings
from weather_forecasting.inference.predictor import Predictor
from weather_forecasting.server.services.weather import WeatherService


def get_weather_service() -> WeatherService:
    return WeatherService()

def get_predictor() -> Predictor:
    return Predictor(model_path= settings.temperature_model_path,
                          feature_path= settings.temperature_feature_path,
                          data_path= settings.processed_path)