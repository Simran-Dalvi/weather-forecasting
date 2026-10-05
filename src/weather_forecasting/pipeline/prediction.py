from weather_forecasting.utils.logger import logger
from weather_forecasting.inference.predictor import Predictor
from weather_forecasting.config.paths import (
    TEMP_MODEL_PATH,
    TEMP_FEATURE_PATH,
    PROCESSED_PATH
)
from weather_forecasting.data.prediction_dataset import save_prediction
from weather_forecasting.pipeline.ingestion import ingest_weather_data
from weather_forecasting.pipeline.processing import processing



def predictor() -> float:
    """
    Complete prediction piepline.

    Steps:
        1. Load the trained model and feature configuration.
        2. Load the latest processed observation.
        3. Validate prediction features.
        4. Run the model.
        5. Save the prediction.
        6. Return the predicted temperature.

    Returns:
        Predicted temperature for the next hour.
    """

    logger.info("Starting next-hour temperature prediction.")

    # Create predictor
    predictor = Predictor(
        model_path= TEMP_MODEL_PATH,
        feature_path= TEMP_FEATURE_PATH,
        data_path= PROCESSED_PATH
    )

    # Generate prediction

    result = predictor.predict()

    prediction_time = result["input_time"]
    prediction = result["prediction"]

    logger.info(
        f"Prediction generated successfully."
        f"Input time: {prediction_time}"
        f"predicted temperature: {prediction:.2f}°C"
    )

    # Save prediction
    save_prediction(
        prediction_time= prediction_time,
        prediction=prediction,
    )

    # Completed !!

    logger.info(
        "next- hour temperature prediction piepline completed successfully."
    )

    return prediction


if __name__ == "__main__":
    ingest_weather_data()
    processing()
    predicted_next_hour_temperature = predictor()

    print(
        f"Predicted temperature for next hour: {predicted_next_hour_temperature:.2f}°C."
    )