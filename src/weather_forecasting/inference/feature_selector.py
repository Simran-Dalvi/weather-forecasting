from weather_forecasting.utils.logger import logger
from pathlib import Path
import pandas as pd

class ProcessedDataLoader:
    def __init__(self, processed_path: Path):
        self.processed_path = processed_path

    def get_latest(self):
        """
        Loads and return the latest processed row for inference.
        """
        try:
            logger.info(f"Loading latest processed features from {self.processed_path}")
            df = pd.read_csv(self.processed_path)
            latest_data = df.tail(1)
            logger.info(f"Loaded {len(latest_data)} row(s) for inference.")
            return latest_data
        except Exception:
            logger.exception("Failed to load processed dataset.")
            raise
