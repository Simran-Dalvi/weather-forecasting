function Forecast(){
    return (
        <div className="space-y-8">
            <div>
            <h1 className="text-3xl font-bold text-gray-900">
                Forecast
            </h1>
            <p className="mt-2 text-gray-500">
                View the next hour temperature prediction.
            </p>
        </div>

        <section>
            <h2 className="text-xl font-semibold text-gray-900">
                Temperature Forecast
            </h2>
            <div className="mt-4 rounded-xl border bg-white p-6">
                <p className="text-gray-500">
                    Forecast data will appear here.
                </p>
            </div>
        </section>
        </div>
    )
}

export default Forecast