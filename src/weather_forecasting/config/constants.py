LATITUDE = 18.52
LONGITUDE = 73.85

HISTORY_DAYS = 365

TEMPERATURE_COL = "Temperature"
HUMIDITY_COL = "Humidity"
WIND_COL = "Wind_Speed"
PRESSURE_COL = "Pressure"
SOIL_MOISTURE_COL = "Soil_Moisture"
SOIL_TEMPERATURE_COL = "Soil_Temp"

LOCATION = {
    "latitude":18.5204,
    "longitude":73.8567,
    "name":"Pune"
    }


REQUIRED_COLUMNS = {
    "date",
    "Temperature",
    "Humidity",
    "Rain",
    "Wind_Speed",
    "Soil_Temp",
    "Soil_Moisture",
    "Pressure",
}

FRESHNESS_THRESHOLD_HOURS = 2
MAXIMUM_FRESHNESS_RETRY = 3
RETRY_DELAYS = [0, 5, 10]