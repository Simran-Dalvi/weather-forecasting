class WeatherForecastingError(Exception):
    """Base Exception for weather forecasting application."""

class WeatherDataNotFoundError(WeatherForecastingError):
    """Raised when required weather data is unavailable."""

class PredictionError(WeatherForecastingError):
    """Raised when weather prediction fails."""