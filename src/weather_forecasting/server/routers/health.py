from fastapi import APIRouter
from weather_forecasting.server.exceptions import WeatherDataNotFoundError, PredictionError

router = APIRouter()

@router.get("/health")
def health():
    return {"status" : "healthy"}

@router.get("/test_data")
async def test_error():
    raise WeatherDataNotFoundError(
        "This is a test error."
    )


@router.get("/test_predict")
async def test_error():
    raise PredictionError(
        "This is a test error."
    )