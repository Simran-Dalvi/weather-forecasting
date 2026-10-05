from fastapi import FastAPI
from weather_forecasting.server.routers.health import router
from weather_forecasting.server.routers.weather import weather_router
from weather_forecasting.server.exceptions import(
    WeatherDataNotFoundError,
    PredictionError
)
from weather_forecasting.server.handlers import (
    weather_data_not_found_handler,
    prediction_error_handler
)


app = FastAPI(title="Weather Forecasting API",
              description="API for weather forecasting application",
              version="0.1.0")

app.add_exception_handler(
    WeatherDataNotFoundError,
    weather_data_not_found_handler
)

app.add_exception_handler(
    PredictionError,
    prediction_error_handler
)

app.include_router(router)

app.include_router(weather_router)