from weather_forecasting.inference.predictor import Predictor
from weather_forecasting.utils.logger import logger
from pathlib import Path
from weather_forecasting.config.paths import TEMPERATURE_1HR_DIR, DATA_DIR
import time
from weather_forecasting.utils.logger import logger


PROCESSED_PATH = DATA_DIR /"processed"/ "processed.csv"
TEMP_MODEL_PATH = TEMPERATURE_1HR_DIR / "Temperature_1_model.pkl"
TEMP_FEATURE_PATH = TEMPERATURE_1HR_DIR / "Temperature_1_features.json"

def predict():
    logger.info("Starting temperature prediction...")
    start_time = time.perf_counter()
    predictor = Predictor(model_path= TEMP_MODEL_PATH,
                           feature_path=TEMP_FEATURE_PATH,
                           data_path= PROCESSED_PATH,)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.debug(f"The predictor took {elapsed_time} time.")

    start_time = time.perf_counter()
    value = predictor.predict()
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    logger.debug(f"The predict function took {elapsed_time}")
    print(value)

if __name__ == "__main__":
    predict()