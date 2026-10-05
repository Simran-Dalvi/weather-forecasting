from pathlib import Path
from weather_forecasting.config.paths import (
    PROCESSED_PATH,
    TEMP_MODEL_PATH,
    TEMP_FEATURE_PATH,
)

class Settings:
    """Application configuration."""

    processed_path: Path = PROCESSED_PATH
    temperature_model_path: Path = TEMP_MODEL_PATH
    temperature_feature_path: Path = TEMP_FEATURE_PATH

settings = Settings()