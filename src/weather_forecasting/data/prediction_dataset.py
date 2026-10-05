from pathlib import Path
import pandas as pd
from weather_forecasting.utils.logger import logger
from weather_forecasting.config.paths import PREDICTIONS_PATH

PREDICTION_COLUMNS = {
    "prediction_time",
    "target_time",
    "temperature_1hr_prediction"
}

def save_prediction(
        prediction_time: pd.Timestamp,
        prediction:float,
        prediction_path: Path = PREDICTIONS_PATH,
) -> None:
    """
    Save a new weather prediction to prediction.csv...

    A prediction is considered a duplicate when a prediction for 
    the same target_time already exists.
    """

    prediction_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    prediction_time = pd.Timestamp(prediction_time)

    if prediction_time.tzinfo is None:
        prediction_time = prediction_time.tz_localize("UTC")
    else:
        prediction_time = prediction_time.tz_convert("UTC") 

    target_time = prediction_time + pd.Timedelta(hours = 1) #come back to this...

    new_prediction = pd.DataFrame(
        [
            {
                "prediction_time": prediction_time,
                "target_time": target_time,
                "temperature_1hr_prediction": float(prediction),
            }
        ]
    )

    if prediction_path.exists():
        existing_prediction = pd.read_csv(prediction_path)

        if not existing_prediction.empty:
            required_columns = PREDICTION_COLUMNS - set(existing_prediction.columns)

            if required_columns:
                raise ValueError("Prediction file is missing required columns:"
                                 f"{sorted(required_columns)}")

            existing_prediction["target_time"] = pd.to_datetime(
                existing_prediction["target_time"],
                utc = True,
            )

            if (
                existing_prediction["target_time"] == target_time
            ).any():

                logger.info(f"Prediction for target time"
                            f"{target_time} already exists."
                            "Skipping duplicate prediction."
                            )
                return

            predictions = pd.concat(
                [existing_prediction, new_prediction],
                ignore_index = True,
            )

    else:
        predictions = new_prediction

    predictions.to_csv(
        prediction_path,
        index = False,
    )

    logger.info(
        f"Prediction saved successfully to {prediction_path}"
    )