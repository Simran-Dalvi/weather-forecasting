from weather_forecasting.features.time import add_time_features
from weather_forecasting.features.temperature import (
    add_temperature_lags, add_temperature_changes, 
    add_temperature_rolling_mean, 
    add_temperature_rolling_std
)
import pandas as pd
from weather_forecasting.config.constants import TEMPERATURE_COL
from weather_forecasting.features.base import BaseFeature
from weather_forecasting.features.humidity import add_humidity_rolling_mean
from weather_forecasting.features.pressure import add_pressure_rolling_mean
from weather_forecasting.features.wind import add_wind_rolling_mean
from weather_forecasting.features.soil_moisture import add_soil_moist_rolling_mean
from weather_forecasting.features.soil_temprature import add_soil_temp_rolling_mean

def build_temperature_1hr_features(df):
    """
    Creates all engineered features required for temprature prediction.
    """

    original_cols = set(df.columns)

    # datetime
    df = add_time_features(df)

    # temprature
    df = add_temperature_lags(df, lags = [1, 2, 3, 6, 12, 24],)

    df = add_temperature_changes(df, periods=[1, 3, 24])

    df = add_temperature_rolling_mean(df, windows=[24])
    df = add_temperature_rolling_std(df, windows=[24])

    # humidity
    df = add_humidity_rolling_mean(df, windows=[24])
    # pressure
    df = add_pressure_rolling_mean(df, windows=[24])
    # wind
    df = add_wind_rolling_mean(df, windows=[24])
    # soil_moisture
    df = add_soil_moist_rolling_mean(df, windows=[24])
    # soil_temprature
    df = add_soil_temp_rolling_mean(df, windows=[24])

    df = BaseFeature.create_target(df, column=TEMPERATURE_COL, horizon=1)

    engineered_columns = [col for col in df.columns if col not in original_cols]

    return df[["date"] + engineered_columns]

if __name__ == "__main__":
    df = build_temperature_1hr_features(df=(pd.read_csv(r"D:\Project\Weather_Forcasting\data\raw\latest_weather.csv")))
    print(df.columns.to_list())