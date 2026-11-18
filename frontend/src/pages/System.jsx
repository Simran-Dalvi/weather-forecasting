function System() {
    return (
        <div className="space-y-6">
            {/* Page Header */}
            <div>
                <h1 className="text-2xl font-bold text-gray-900">
                    System Monitoring
                </h1>
                <p className="mt-1 text-sm text-gray-500">
                    Monitor the health and operational status of your weather forecasting system.
                </p>
            </div>

            {/* Overall System Status */}
            <section className="rounded-xl border border-gray-200 bg-green-200 p-6 shadow-sm">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <p className="text-sm font-medium text-gray-500">
                            Overall System Status
                        </p>
                        <h2 className="mt-2 text-2xl font-bold text-gray-900">
                            System Operational
                        </h2>
                        <p className="mt-1 text-sm text-gray-500">
                            the monitoring dashboard is waiting live system health data.
                        </p>
                    </div>

                    <div className="flex item-center gap-2 self-start rounded-full bg-green-100 px-4 py-2">
                        <span className="h-2.5 w-2.5 rounded-ful bg-green-500"></span>
                        <span className="text-sm font-semifold text-green-700">
                            Demo Status
                        </span>
                    </div>

                </div>
            </section>

            {/* System Metrics */}
            <section className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">

                {/* API Health */}
                <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-md">
                    <div className="flex items-center justify-between">
                        <h3 className="text-sm font-medium text-gray-500">
                            API Health
                        </h3>
                        <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">
                            Not Connected
                        </span>
                    </div>

                    <p className="mt-4 text-2xl font-bold text-shadow-gray-900">
                        --
                    </p>
                    <p className="mt-1 text-sm text-gray-500">
                        Backend Availability
                    </p>
                </div>

                {/* Pipeline Status*/}
                <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-md">
                    <div className="flex items-center justify-between">
                        <h3 className="text-sm font-medium text-gray-500">
                            Pipeline Status
                        </h3>
                        <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">
                            Not Connected
                        </span>
                    </div>

                    <p className="mt-4 text-2xl font-bold text-shadow-gray-900">
                        --
                    </p>
                    <p className="mt-1 text-sm text-gray-500">
                        Last successful execution
                    </p>
                </div>

                {/* Data Freshness */}
                <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-md">
                    <div className="flex items-center justify-between">
                        <h3 className="text-sm font-medium text-gray-500">
                            Data Freshness
                        </h3>
                        <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">
                            Not Connected
                        </span>
                    </div>

                    <p className="mt-4 text-2xl font-bold text-shadow-gray-900">
                        __
                    </p>
                    <p className="mt-1 text-sm text-gray-500">
                        Latest weather observation
                    </p>
                </div>
            </section>

            {/* Model Information */}
            <section className="rounded-xl border border-gray-200 bg-emerald-200 p-6 shadow-sm">

                <div className="mb-5">
                    <h2 className="text-lg font-semibold text-gray-900">
                        Model Information
                    </h2>
                    <p className="mt-1 text-sm text-gray-500">
                        Details about the active weather forecasting model.
                    </p>
                </div>

                <div className="grid rounded-2xl bg-white p-4 shadow-t-xl grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-4">

                    <div>
                        <p className="text-sm text-gray-500">Model Name</p>
                        <p className="mt-2 font-semibold text-gray-900">
                            Temperature 1-Hour Model
                        </p>
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">Prediction Target</p>
                        <p className="mt-2 font-semibold text-gray-900">
                            Temperature
                        </p>
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">Prediction Horizon</p>
                        <p className="mt-2 font-semibold text-gray-900">
                            1 Hour Ahead
                        </p>
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">Data Source</p>
                        <p className="mt-2 font-semibold text-gray-900">
                            Open-Meteo
                        </p>
                    </div>

                </div>
            </section>

            {/* Recent Activity */}
            <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">

                <div className="mb-5">
                    <h2 className="text-lg font-semibold text-gray-900">
                        Recent Activity
                    </h2>
                    <p className="mt-1 text-sm text-gray-500">
                        Recent system events and pipeline activity.
                    </p>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full min-w-150 text-left">

                        <thead>
                            <tr className="border-b border-gray-200 text-sm text-gray-500">
                                <th className="pb-3 font-medium">Event</th>
                                <th className="pb-3 font-medium">Description</th>
                                <th className="pb-3 font-medium">Timestamp</th>
                                <th className="pb-3 font-medium">Status</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr>
                                <td colSpan="4" className="py-8 text-center text-sm text-gray-400">
                                    No recent activity available.
                                </td>
                            </tr>
                        </tbody>

                    </table>
                </div>
            </section>

        </div>
    )
}

export default System