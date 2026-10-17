from weather_forecasting.server.services.weather import WeatherService

def get_weather_service() -> WeatherService:
    return WeatherService()