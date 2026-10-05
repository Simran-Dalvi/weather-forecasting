import pandas as pd
import pytest

from weather_forecasting.inference.predictor import Predictor
from weather_forecasting.server.exceptions import PredictionError

class FakeModel:
    def predict(self, features):
        return [25.5]

class FakeModelLoader:
    def __init__(self, feature_order):
        self.feature_order = feature_order

    def load(self):
        return FakeModel(), self.feature_order

class FakeDataLoader:
    def __init__(self, latest_df):
        self.latest_df = latest_df

    def get_latest(self):
        return self.latest_df

def create_predictor(monkeypatch, feature_order, latest_df):
    monkeypatch.setattr(
        "weather_forecasting.inference.predictor.ModelLoader",
        lambda model_path, feature_path: FakeModelLoader(feature_order),
    )

    monkeypatch.setattr(
        "weather_forecasting.inference.predictor.ProcessedDataLoader",
        lambda data_path: FakeDataLoader(latest_df),
    )

    return Predictor(
        model_path = "fake_model.pkl",
        feature_path = "fake_features.json",
        data_path = "fake_data.csv",
    )

"""***************"""

def test_prepare_features(monkeypatch):
    feature_order = ["Temperature", "Humidity"]

    latest_df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-09-10 10:00:00"]),
            "Temperature": [25.0],
            "Humidity": [70.0],
        }
    )

    predictor = create_predictor(
        monkeypatch,
        feature_order,
        latest_df,
    )

    features, input_time = predictor.prepare_features()

    assert list(features.columns) == feature_order
    assert features.shape == (1,2)
    assert features.iloc[0]["Temperature"] == 25.0
    assert features.iloc[0]["Humidity"] == 70.0
    assert input_time == pd.Timestamp("2026-09-10 10:00:00")

def test_predict(monkeypatch):
    feature_order = ["Temperature", "Humidity"]

    latest_df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-09-10 10:00:00"]),
            "Temperature": [25.0],
            "Humidity": [70.0],
        }
    )

    predictor = create_predictor(
        monkeypatch,
        feature_order,
        latest_df,
    )

    result = predictor.predict()

    assert result["prediction"] == 25.5
    assert result["input_time"] == pd.Timestamp("2026-09-10 10:00:00")

def test_missing_features_raises_prediction_error(monkeypatch):
    feature_order = ["Temperature", "Humidity"]

    latest_df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-09-10 10:00:00"]),
            "Temperature": [25.0],
        }
    )

    predictor = create_predictor(
        monkeypatch,
        feature_order,
        latest_df
    )

    with pytest.raises(PredictionError):
        predictor.predict()

def test_nan_features_raises_prediction_error(monkeypatch):
    feature_order = ["Temperature", "Humidity"]

    latest_df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-09-10 10:00:00"]),
            "Temperature": [25.0],
            "Humidity": [None],
        }
    )

    predictor = create_predictor(
        monkeypatch,
        feature_order,
        latest_df
    )

    with pytest.raises(PredictionError):
        predictor.predict()

def test_model_failure_raises_prediction_error(monkeypatch):
    feature_order = ["Temperature", "Humidity"]

    latest_df = pd.DataFrame({
        "date": pd.to_datetime(["2026-09-10 10:00:00"]),
        "Temperature": [25.0],
        "Humidity": [70.0],
    })

    predictor = create_predictor(
        monkeypatch,
        feature_order,
        latest_df,
    )

    class FailingModel:
        def predict(self, features):
            raise RuntimeError("Model prediction failed")

    predictor.model = FailingModel()

    with pytest.raises(PredictionError):
        predictor.predict()