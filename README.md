# Weather Forecasting System 🌦️

A modular weather forecasting pipeline built with Python that fetches
weather data from the Open-Meteo API, performs preprocessing and feature
engineering, and prepares datasets for machine learning models.

The long-term goal of this project is to predict future weather
conditions (starting with next-hour temperature prediction) using
machine learning while maintaining a production-ready pipeline that can
later be automated.

---

There are some later production-hardening concerns—atomic file writes, retry policies, cache behavior, monitoring/alerts, etc.—but I would not pile those onto ingestion.py right now.

---

## Project Goals

-   Collect real-time weather data
-   Build reusable feature engineering pipelines
-   Train multiple forecasting models
-   Generate weather predictions
-   Deploy prediction pipeline for production use

## Current Progress

-   ✅ Data collection from Open-Meteo API
-   ✅ Raw dataset storage
-   ✅ Processed dataset management
-   ✅ Modular feature engineering pipeline
-   ✅ Logging system
-   🚧 Model training (In Progress)
-   🚧 Prediction pipeline
-   🚧 Deployment

## Project Architecture

``` text
Weather API
     │
     ▼
Raw Data
     │
     ▼
Preprocessing
     │
     ▼
Feature Engineering
     │
     ▼
Model Training
     │
     ▼
Inference
     │
     ▼
Predictions
```

Overall ML workflow:

``` text
Data
   ↓
Features
   ↓
Training
   ↓
Inference
```

## Project Structure

``` text
weather_forecasting/
│
├── api/
├── data/
│   ├── raw/
│   └── processed/
├── feature_pipelines/
├── feature_store/
├── inference/
├── models/
├── utils/
├── tests/
├── config.py
└── main.py
```

## Pipeline Overview

### 1. Data Collection

-   Connect to Open-Meteo API
-   Download hourly weather data
-   Validate API response
-   Handle API errors
-   Return a pandas DataFrame

**Output**

``` text
data/raw/weather_raw.csv
```

### 2. Data Preprocessing

-   Convert dates
-   Sort by datetime
-   Remove duplicate records
-   Handle missing values
-   Correct data types
-   Reset index

**Output**

``` text
data/processed/weather_clean.csv
```

### 3. Feature Engineering

-   Hour
-   Day
-   Month
-   Cyclical encoding
-   Lag features
-   Rolling statistics
-   Derived weather features
-   Target variable

**Output**

``` text
data/processed/temperature_features.csv
```

Each model has its own feature pipeline while reusing common feature
builders.

### 4. Model Training

*Currently under development.*

-   Split data
-   Train model(s)
-   Evaluate performance
-   Save trained models

Future models:

-   Linear Regression
-   Random Forest
-   XGBoost
-   LightGBM
-   CatBoost

Saved models:

``` text
models/
```

### 5. Inference

> **Important**
>
> The `inference` folder should only contain code responsible for
> loading a trained model and generating predictions.
>
> It should **not** perform:
>
> -   Data collection
> -   Data cleaning
> -   Feature engineering
> -   Model training
>
> At the moment, this project does **not** include inference because no
> trained production model exists yet.

Future inference flow:

-   Load latest weather data
-   Load trained model
-   Predict next-hour temperature

### 6. Pipeline

``` text
Fetch data
    ↓
Store raw data
    ↓
Clean data
    ↓
Feature engineering
    ↓
Load trained model
    ↓
Predict
    ↓
Save prediction
```

### 7. Logging

Logging tracks:

-   API status
-   Data loading
-   Feature engineering
-   Pipeline execution
-   Errors
-   Warnings

### 8. Configuration

All project settings are centralized in:

``` text
config.py
```

Examples:

-   File paths
-   API parameters
-   Feature settings
-   Model configuration
-   Project directories

### 9. Testing

Unit tests will cover:

-   API
-   Data preprocessing
-   Feature engineering
-   Model training
-   Prediction pipeline

### 10. Automation (Future)

``` text
Every hour
     ↓
Fetch latest weather
     ↓
Generate features
     ↓
Load trained model
     ↓
Predict
     ↓
Store prediction
     ↓
Send prediction to application
```

Possible schedulers:

-   Cron
-   Windows Task Scheduler
-   Apache Airflow

## Technologies Used

-   Python
-   Pandas
-   NumPy
-   Open-Meteo API
-   Scikit-learn
-   Logging
-   UV
-   Git

Future:

-   LightGBM
-   XGBoost
-   CatBoost
-   FastAPI
-   Docker

## Current Status

-   ✅ Data collection
-   ✅ Raw data storage
-   ✅ Processed dataset management
-   ✅ Modular feature engineering
-   ✅ Logging
-   🚧 Model training
-   🚧 Inference
-   🚧 Automation
-   🚧 Deployment

## Future Improvements

-   Train multiple forecasting models
-   Hyperparameter tuning
-   Feature selection
-   Multi-step forecasting
-   REST API for predictions
-   Docker deployment
-   CI/CD pipeline
-   Automated hourly forecasting
-   Dashboard integration


--------

The roadmap I'd follow is:

Finish the inference pipeline
Ensure prediction works end-to-end with the latest processed data.
Eliminate any remaining feature mismatch issues.
Build a service layer
Wrap the predictor in a reusable API (for example, with FastAPI).
Separate business logic from the web layer.
Develop the frontend
Display current weather and predicted temperature.
Show charts and key metrics in a clean interface.
Automate the pipeline
Fetch new weather data on a schedule.
Update processed features.
Generate fresh predictions automatically.
Deploy the application
Host the API.
Deploy the frontend.
Make the application publicly accessible.
Version 2 enhancements
Extend forecasting from 1 hour to 24 hours and eventually 7 days.
Add humidity, rainfall, and wind predictions.
Incorporate model monitoring and retraining workflows.