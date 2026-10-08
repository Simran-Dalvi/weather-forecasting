function Dashboard() {
    return (
        <div className="space-y-8">
            <header className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
                        Weather Intelligence
                    </h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Updated 5 minutes ago
                    </p>
                </div>

                <div className="text-left sm:text-right">
                    <p className="text-sm font-medium text-gray-900">
                        Pune, India
                    </p>

                    <p className="text-xs text-gray-500">
                        Asia/Kolkata
                    </p>
                </div>
            </header>

            <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <div className="rounded-xl border bg-green-200">
                    <p className="text-sm text-gray-500 px-3">
                        Current Temperature
                    </p>
                    <p className="mt-2 text-2xl font-bold text-gray-900 px-3">
                        28.4°C
                    </p>
                </div>
                <div className="rounded-xl border bg-green-200">
                    <p className="text-sm text-gray-500 px-3">
                        Humidity
                    </p>
                    <p className="mt-2 text-2xl font-bold text-gray-900 px-3">
                        72%
                    </p>
                </div>
                <div className="rounded-xl border bg-green-200">
                    <p className="text-sm text-gray-500 px-3">
                        Rainfall
                    </p>
                    <p className="mt-2 text-2xl font-bold text-gray-900 px-3">
                        0.0 mm
                    </p>
                </div>
                <div className="rounded-xl border bg-green-200">
                    <p className="text-sm text-gray-500 px-3">
                        Wind Speed
                    </p>
                    <p className="mt-2 text-2xl font-bold text-gray-900 px-3">
                        12 km/h
                    </p>
                </div>
            </section>

            <section className="rounded-xl border bg-white p-6 sm:p-8">
                <div className="text-center">
                    <p className="text-sm font-medium uppercase tracking-wider text-gray-500">
                        Next-Hour Temperature
                    </p>

                    <p className="mt-4 text-5xl font-bold tracking-tight text-gray-900">
                        29.1°C
                    </p>

                    <p className="mt-2 text-sm text-gray-500">
                        Expected at 6:00 pm
                    </p>
                </div>
            </section>
        </div>
    )
}

export default Dashboard