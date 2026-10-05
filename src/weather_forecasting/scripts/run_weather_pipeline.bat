@echo off

cd /d D:\Project\Weather_Forcasting

echo Starting weather forcasting pipeline

uv run python -m weather_forecasting.pipeline.run_pipeline

if %ERRORLEVEL% NEQ 0 (
    echo Pipeline FAILED
    exit /b %ERRORLEVEL%
)

echo Pipeline completed successfully.