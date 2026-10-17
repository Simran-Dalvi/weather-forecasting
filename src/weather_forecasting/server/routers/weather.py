from fastapi import APIRouter, Depends

from weather_forecasting.server.dependencies import get_weather_service
from weather_forecasting.server.schemas.weather import WeatherPredictionResponse, CurrentWeatherResponse
from weather_forecasting.server.services.weather import WeatherService

weather_router = APIRouter(
    prefix = "/weather",
    tags = ["Weather"],
)

@weather_router.get(
    "/current",
    response_model= CurrentWeatherResponse
)
def get_current_weather(
    weather_service: WeatherService = Depends(get_weather_service)
) -> CurrentWeatherResponse:
    return weather_service.get_current_weather()

@weather_router.get(
    "/predict",
    response_model = WeatherPredictionResponse,
)
def predict_weather(
    weather_service: WeatherService = Depends(get_weather_service),
) -> WeatherPredictionResponse:
    return weather_service.predict_next_hour()
