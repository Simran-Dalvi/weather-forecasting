from fastapi import Request
from fastapi.responses import JSONResponse

from weather_forecasting.server.exceptions import (
    WeatherDataNotFoundError,
    PredictionError,
    PredictionUnavailableError
)

async def weather_data_not_found_handler(
        request: Request,
        exc: WeatherDataNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code= 404,
        content={
            "error": "weather_data_not_found",
            "message": str(exc),
        },
    )

async def prediction_error_handler(
        request: Request,
        exc: PredictionError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "prediction_error",
            "message": str(exc),
        }
    )

async def prediction_unavailable_handler(
        request: Request,
        exc: PredictionUnavailableError,
) -> JSONResponse:
    return JSONResponse(
        status_code = 503,
        content={
            "error": "prediction_unavailable",
            "message": str(exc),
        },
    )