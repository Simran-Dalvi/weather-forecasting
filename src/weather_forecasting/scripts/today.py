# from weather_forecasting.data.raw_dataset import load_today_data

# df = load_today_data()

# print(df)
# print(df.shape)
# print(df["date"].min())
# print(df["date"].max())

import pandas as pd
from weather_forecasting.config.paths import DATA_DIR
from pathlib import Path

PROCESSED_STORE_PATH = DATA_DIR /"processed"/ "processed.csv"

df = pd.read_csv(PROCESSED_STORE_PATH)

print(df.columns.tolist())
print()
print(df.tail(2))
print()
print(df.tail(2)[[
    "date",
    "Temperature",
    "target_Temperature_1"
]])