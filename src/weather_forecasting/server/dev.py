import os

import uvicorn

def main():
    os.environ["PYTHONUTF8"] = "1"
    os.environ["PYTHONENCODING"] = "utf-8"

    uvicorn.run(
        "weather_forecasting.server.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

if __name__ == "__main__":
    main()