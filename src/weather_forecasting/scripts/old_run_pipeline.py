from weather_forecasting.scripts.fetch_weather_data import fetch_weather_data
from weather_forecasting.scripts.feature_engineering import feature_engineering
from weather_forecasting.scripts.predict import predict

def main():
    fetch_weather_data()
    feature_engineering()
    predict()


if __name__ == "__main__":
    main()