from fastapi.testclient import TestClient

from weather_forecasting.server.main import app
from weather_forecasting.server.dependencies import (
    get_weather_service,
    get_predictor,
    )

class FakeWeatherService:

    def get_current_weather(self):
        return {
            "source": "Open-Meteo API", 
            "location": {
                "name": "Pune", 
                "latitude": 18.5204, 
                "longitude": 73.8567, }, 
                "hourly": [ 
                    { 
                        "timestamp": "2026-09-12T10:00:00+00:00", 
                        "temperature": 25.0, 
                        "humidity": 70.0, 
                        "rain": 0.0, 
                        "wind_speed": 10.0, 
                        "soil_temperature": 24.0, 
                        "soil_moisture": 30.0, 
                        "pressure": 1012.0, 
                    } 
                ],
        }


def test_current_weather():
    app.dependency_overrides[get_weather_service] = (
        lambda: FakeWeatherService()
    )

    client = TestClient(app)

    response = client.get("/weather/current")

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "Open-Meteo API"
    assert data["location"]["name"] == "Pune"
    assert len(data["hourly"]) == 1
    assert data["hourly"][0]["temperature"] == 25.0

    app.dependency_overrides.clear()

def test_current_weather_no_data():
    class EmptyWeatherService:

        def get_current_weather(self):
            from weather_forecasting.server.exceptions import (
                WeatherDataNotFoundError,
            )

            raise WeatherDataNotFoundError(
                "No weather data available for today."
            )

    app.dependency_overrides[get_weather_service] = (
        lambda: EmptyWeatherService()
    )

    client = TestClient(app)

    response = client.get("/weather/current")

    assert response.status_code == 404

    data = response.json()

    assert data["error"] == "weather_data_not_found"
    assert data["message"] == "No weather data available for today."

    app.dependency_overrides.clear()


def test_predict_weather():

    class FakeWeatherService:

        def predict_next_hour(self, predictor):
                return {
                    "generated_at": "2026-09-12T10:00:00+00:00",
                    "location": {
                        "name": "Pune",
                        "latitude": 18.5204,
                        "longitude": 73.8567,
                    },
                    "predictions":[
                        {
                            "target_time": "2026-09-12T11:00:00+00:00",
                            "predictions": {
                                "temperature":26.5,
                                "humidity": None,
                                "rain": None,
                                "wind_speed": None,
                                "soil_temperature": None,
                                "soil_moisture": None,
                                "pressure": None,
                            },
                        }
                    ],
                }

    class FakePredictor:
        pass

    app.dependency_overrides[get_weather_service] = (
        lambda: FakeWeatherService()
    )

    app.dependency_overrides[get_predictor] = (
        lambda: FakePredictor()
    )

    client = TestClient(app)

    response = client.get("/weather/predict")

    assert response.status_code == 200

    data = response.json()

    assert data["location"]["name"] == "Pune"
    assert len(data["predictions"]) == 1
    assert data["predictions"][0]["predictions"]["temperature"] == 26.5

    app.dependency_overrides.clear()


def test_predict_weather_failure():

    class EmptyWeatherPredict:

        def predict_next_hour(self, predictor):
            from weather_forecasting.server.exceptions import PredictionError

            raise PredictionError(
                "Failed to generate weather prediction during inference."
            )

    app.dependency_overrides[get_weather_service] = (
        lambda: EmptyWeatherPredict()
    )
    

    client = TestClient(app)

    response = client.get("/weather/predict")

    assert response.status_code == 500

    data = response.json()

    assert data["error"] == "prediction_error"
    assert data["message"] == "Failed to generate weather prediction during inference."

    app.dependency_overrides.clear()