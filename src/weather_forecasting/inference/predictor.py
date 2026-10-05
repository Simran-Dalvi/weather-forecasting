from pathlib import Path

import pandas as pd

from weather_forecasting.inference.feature_selector import ProcessedDataLoader
from weather_forecasting.inference.model_loader import ModelLoader
from weather_forecasting.utils.logger import logger
from weather_forecasting.server.exceptions import PredictionError

class Predictor:
    def __init__(
            self,
            model_path: Path,
            feature_path: Path,
            data_path: Path,
    ) -> None:
        model_loader = ModelLoader(model_path, feature_path)

        self.data_loader = ProcessedDataLoader(data_path)
        self.model, self.feature_order = model_loader.load()

    def prepare_features(
            self,
    ) -> tuple[pd.DataFrame, pd.Timestamp]:
        """Prepare the latest feature required for prediction."""
        logger.info("Prepare features")

        latest_df = self.data_loader.get_latest()

        missing = set(self.feature_order) - set(latest_df.columns)
        if missing:
            raise ValueError(
                f"Missing features in data: {sorted(missing)}"
            )

        features = latest_df[self.feature_order]

        if features.isna().any().any():
            nan_columns = features.columns[
                features.isna().any()
            ].tolist()

            logger.error(
                f"NaN values found in columns: {nan_columns}"
            )
            logger.error(
                f"Feature values: \n {features[nan_columns]}"
            )

            raise ValueError(
                "Latest feature row contains NaN values."
            )

        input_time = latest_df["date"].iloc[0]

        logger.info("Features prepared successfully.")

        return features, input_time

    def predict(self) -> dict[str, float | pd.Timestamp]:
        """Generate a prediction using the latest available features."""
        logger.info("Running model prediction")

        try:
            features, input_time = self.prepare_features()

            prediction = self.model.predict(features)

            logger.info("Prediction completed successfully.")

            return {
                "input_time": input_time,
                "prediction": float(prediction[0]),
            }

        except Exception as exc:
            logger.exception(
                "Failed to generate weather prediction during inference."
            )

            raise PredictionError(
                "Failed to generate weather prediction during inference."
            ) from exc