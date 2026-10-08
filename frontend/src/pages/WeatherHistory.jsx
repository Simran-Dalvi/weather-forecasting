function WeatherHistory() {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">
                    Weather History
                </h1>
                <p className="mt-2 font-bold text-gray-500">
                    Explore historical weather observations and predictions.
                </p>
            </div>

            <section>
                <h2 className="text-xl font-semibold text-gray-900">
                    Historical Weather
                </h2>
                <div className="mt-4 rounded-xl border bg-white p-6">
                    <p className="text-gray-500">
                        Historical weather data will appear here.
                    </p>
                </div>
            </section>
        </div>
    )
}

export default WeatherHistory