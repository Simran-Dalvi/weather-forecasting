from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"

MODELS_DIR = PROJECT_ROOT / "models"

TEMPERATURE_1HR_DIR = MODELS_DIR / "temperature" / "1hr"


PROCESSED_PATH = DATA_DIR /"processed"/ "processed.csv"
PREDICTIONS_PATH = DATA_DIR /"predictions"/ "predictions.csv"
TEMP_MODEL_PATH = TEMPERATURE_1HR_DIR / "Temperature_1_model.pkl"
TEMP_FEATURE_PATH = TEMPERATURE_1HR_DIR / "Temperature_1_features.json"