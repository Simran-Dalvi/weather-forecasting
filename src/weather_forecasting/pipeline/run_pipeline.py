from weather_forecasting.utils.logger import logger
from weather_forecasting.pipeline.ingestion import ingest_weather_data
from weather_forecasting.pipeline.processing import processing
from weather_forecasting.pipeline.prediction import predictor

def run_pipeline():
    logger.info("Starting weather forecasting piepline.")

    try:
        logger.info("STEP 1: Ingestion")
        ingest_weather_data()

        logger.info("STEP 2: Processing")
        processing()

        logger.info("STEP 3: Prediction")
        predictor()

        logger.info("Weather forecasting piepline completed successfully.")

    except Exception:
        logger.exception("Weather forecasting piepline failed.")
        raise

if __name__ == "__main__":
    run_pipeline()