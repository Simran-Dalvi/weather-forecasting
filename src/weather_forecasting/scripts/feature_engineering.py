from weather_forecasting.data.raw_dataset import load_latest_data
from weather_forecasting.data.processed_dataset import update_processed_dataset
from weather_forecasting.features.feature_pipeline.temperature_1hr import build_temperature_1hr_features
from weather_forecasting.utils.logger import logger

def feature_engineering():
    """
    Build all engineered features and update the master processed dataset.
    """

    logger.info("Starting feature engineering pipeline...")

    try:
        # Load raw dataset
        logger.info("Loading raw dataset...")

        try:
            raw_df = load_latest_data()
        except FileNotFoundError:
            logger.exception("Raw dataset not found.")
            raise

        # Temprature Features
        logger.info("Building temperature 1-hour features...")

        temperature_features = build_temperature_1hr_features(raw_df)

        logger.info("Updating processed dataset with temprature features...")
        
        update_processed_dataset(
            new_features= temperature_features,
            raw_df = raw_df     # Only used if processed.csv dosen't exist
        )

        logger.info("Feature engineering pipeline completed successfully.")
    except:
        logger.exception("Feature engineering pipeline failed.")
        raise


if __name__ == "__main__":
    feature_engineering()