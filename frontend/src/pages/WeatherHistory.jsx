function WeatherHistory() {
    return (
        <div className="space-y-8">
            {/* Page Header */}
            <header>
                <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
                    Weather History
                </h1>
                <p className="mt-1 text-sm text-gray-500">
                    Explore historical weather observations and trends.
                </p>
            </header>

            {/* Historical Summary */}
            <section>
                <h2 className="mb-4 text-lg font-semibold text-shadow-gray-900">
                    Weather Summary
                </h2>

                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">

                    <div className="rounded-xl border border-gray-200  bg-green-200 p-5">
                        <p className="text-sm text-gray-500">
                            Average Temperature
                        </p>
                        <p className="mt-2 text-2xl font-bold text-gray-900">
                            --°C
                        </p>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default WeatherHistory