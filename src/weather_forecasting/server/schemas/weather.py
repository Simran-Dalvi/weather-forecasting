from datetime import datetime
from pydantic import BaseModel

class Location(BaseModel):
    latitude: float
    longitude: float
    name: str | None = None

class RainPrediction(BaseModel):
    probability: float
    expected_amount: float | None = None


class WeatherObservation(BaseModel):
    timestamp: datetime
    temperature: float | None = None
    humidity: float |None = None
    rain: float |None = None
    wind_speed: float | None = None
    soil_temperature: float | None = None
    soil_moisture: float | None = None
    pressure: float | None = None

class WeatherHistoryPoint(BaseModel):
    timestamp: datetime
    temperature: float | None = None
    humidity: float |None = None
    rain: float |None = None
    wind_speed: float | None = None
    soil_temperature: float | None = None
    soil_moisture: float | None = None
    pressure: float | None = None

class WeatherHistoryResponse(BaseModel):
    source: str
    location: Location
    data: list[WeatherHistoryPoint]

class WeatherPrediction(BaseModel):
    temperature: float | None = None
    humidity: float |None = None
    rain: RainPrediction |None = None
    wind_speed: float | None = None
    soil_temperature: float | None = None
    soil_moisture: float | None = None
    pressure: float | None = None

class WeatherPredictionPoint(BaseModel):
    target_time: datetime
    predictions: WeatherPrediction

class WeatherPredictionResponse(BaseModel):
    generated_at: datetime
    location: Location
    predictions: list[WeatherPredictionPoint]

class CurrentWeatherResponse(BaseModel):
    # timestamp: datetime
    source: str
    location: Location
    hourly: list[WeatherObservation]