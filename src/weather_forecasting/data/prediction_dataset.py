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

    predictions = new_prediction

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

    # else:
    #     predictions = new_prediction

    predictions.to_csv(
        prediction_path,
        index = False,
    )

    logger.info(
        f"Prediction saved successfully to {prediction_path}"
    )

def load_latest_prediction(
    now_utc: pd.Timestamp | None = None,
) -> dict:
    """Load the latest saved prediction if its target time is in the future."""

    if not PREDICTIONS_PATH.exists():
        raise FileNotFoundError(
            f"Prediction dataset not found: {PREDICTIONS_PATH}. "
            "Run the weather forecasting pipeline first."
        )

    df = pd.read_csv(PREDICTIONS_PATH)

    if df.empty:
        raise ValueError("The prediction dataset is empty.")

    required_columns = {
        "prediction_time",
        "target_time",
        "temperature_1hr_prediction",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Prediction dataset is missing columns: {missing_columns}"
        )

    df["prediction_time"] = pd.to_datetime(
        df["prediction_time"], utc=True, errors="coerce"
    )
    df["target_time"] = pd.to_datetime(
        df["target_time"], utc=True, errors="coerce"
    )
    df["temperature_1hr_prediction"] = pd.to_numeric(
        df["temperature_1hr_prediction"], errors="coerce"
    )

    df = df.dropna(
        subset=[
            "prediction_time",
            "target_time",
            "temperature_1hr_prediction",
        ]
    )

    if df.empty:
        raise ValueError("No valid saved predictions were found.")

    # Find the most recently generated prediction.
    latest = df.sort_values("prediction_time").iloc[-1]

    # Use the current UTC time unless a test supplies a fixed time.
    if now_utc is None:
        now_utc = pd.Timestamp.now(tz="UTC")
    else:
        now_utc = pd.Timestamp(now_utc)

    if now_utc.tzinfo is None:
        raise ValueError("now_utc must be timezone-aware.")

    now_utc = now_utc.tz_convert("UTC")

    # Never return a prediction for a target time that has passed.
    if latest["target_time"] <= now_utc:
        raise ValueError(
            "The latest saved prediction has expired. "
            "Run the weather forecasting pipeline to generate a new prediction."
        )

    return latest.to_dict()
