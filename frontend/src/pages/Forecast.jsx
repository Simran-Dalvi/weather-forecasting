import WeatherChart from "../components/WeatherChart"

const forecastData = [
    { time: "12 PM", temperature: 27.2 },
    { time: "1 PM", temperature: 27.8 },
    { time: "2 PM", temperature: 28.1 },
    { time: "3 PM", temperature: 27.6 },
    { time: "4 PM", temperature: 28.3 },
]

function Forecast(){
    return (
        <div className="space-y-8">
            {/* Page Header */}
            <header>
                <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
                    Weather Forecast
                </h1>

                <p className="mt-1 text-sm text-gray-500">
                    Model-based weather prediction for Pune, India.
                </p>
            </header>

            {/* Main Prediction */}
            <section className="rounded-2xl border">
                <div className="text-center">
                    <p className="text-sm font-medium uppercase tracking-wider text-gray-500">
                        Next-Hour Temperature Prediction
                    </p>
                    <p className="mt-4 text-5xl font-bold tracking-tight text-shadow-gray-900">
                        --°C
                    </p>
                    <p className="mt-2 text-sm text-gray-500">
                        Expected at --
                    </p>
                </div>
            </section>

            {/* Forecast Information */}
            <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <div className="rounded-xl border border-gray-200 bg-green-200 p-5">
                    <p className="text-sm text-gray-500">
                        Prediction Time
                    </p>
                    <p className="mt-2 text-lg font-semibold text-gray-900">
                        --
                    </p>
                    <p className="mt-1 text-xs text-gray-400">
                        Last model execution
                    </p>
                </div>

                <div className="rounded-xl border border-gray-200 bg-green-200 p-5">
                    <p className="text-sm text-gray-500">
                        Target Time
                    </p>
                    <p className="mt-2 text-lg font-semibold text-gray-900">
                        --
                    </p>
                    <p className="mt-1 text-xs text-gray-400">
                        Expected prediction time
                    </p>
                </div>

                <div className="rounded-xl border border-gray-200 bg-green-200 p-5">
                    <p className="text-sm text-gray-500">
                        Forecast Horizon
                    </p>
                    <p className="mt-2 text-lg font-semibold text-gray-900">
                        1 hour
                    </p>
                    <p className="mt-1 text-xs text-gray-400">
                        Prediction Interval
                    </p>
                </div>

                <div className="rounded-xl border border-gray-200 bg-green-200 p-5">
                    <p className="text-sm text-gray-500">
                        Model
                    </p>
                    <p className="mt-2 text-lg font-semibold text-gray-900">
                        Temperature
                    </p>
                    <p className="mt-1 text-xs text-gray-400">
                        Logistic Regression
                    </p>
                </div>
            </section>

            {/* Temperature Forecast Chart */}
            <section>
                <WeatherChart
                    title="Temperature Trend"
                    data={forecastData}
                    dataKey="temperature"
                    color="#F97316"
                    unit="°C"
                />
            </section>

            {/* Model Information */}
            <section className="rounded-2xl border border-gray-200 bg-white p-6 sm:p-8">
                <div>
                    <h2 className="text-lg font-semibold text-gray-900">
                        Model Information
                    </h2>
                    <p className="mt-1 text-sm text-gray-500">
                        Details about the temperature forecasting model.
                    </p>
                </div>

                <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
                    <div>
                        <p className="text-sm text-gray-500">
                            Prediction Target
                        </p>
                        <p className="mt-1 font-medium text-gray-900">
                            Temperature
                        </p>
                    </div>
                    <div>
                        <p className="text-sm text-gray-500">
                            Prediction Horizon
                        </p>
                        <p className="mt-1 font-medium text-gray-900">
                            1 Hour Ahead
                        </p>
                    </div>
                    <div>
                        <p className="text-sm text-gray-500">
                            Model Type
                        </p>
                        <p className="mt-1 font-medium text-gray-900">
                            Machine Learning Regression
                        </p>
                    </div>
                    <div>
                        <p className="text-sm text-gray-500">
                            Data Source
                        </p>
                        <p className="mt-1 font-medium text-gray-900">
                            Open-Meteo
                        </p>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default Forecast