from pathlib import Path
import json
import joblib
from weather_forecasting.utils.logger import logger

class ModelLoader:
    """
    Loads a trained model and its feature order.
    """

    def __init__(self, model_path: Path, feature_path: Path):
        self.model_path = Path(model_path)
        self.feature_path = Path(feature_path)

    def load_model(self):        
        logger.info("Loading trained model...")
        model = joblib.load(self.model_path)
        logger.info("Model loaded successfully.")
        return model
    
    def load_feature_order(self):
        logger.info("Loading feature order...")
        with open(self.feature_path, "r") as f:
            feature = json.load(f)
        logger.info(f"Loaded {len(feature)} features.")
        return feature
        
    def load(self):
        model = self.load_model()
        feature_order = self.load_feature_order()

        return model, feature_order