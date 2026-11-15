import { useState } from "react"

import WeatherChart from "../components/WeatherChart"


// Temporary historical data for frontend design
const historicalData = [
    { time: "10 Nov", temperature: 26, humidity: 65, rainfall: 0.5 },
    { time: "11 Nov", temperature: 27, humidity: 62, rainfall: 0 },
    { time: "12 Nov", temperature: 25, humidity: 70, rainfall: 1.2 },
    { time: "13 Nov", temperature: 28, humidity: 60, rainfall: 0 },
    { time: "14 Nov", temperature: 27, humidity: 64, rainfall: 0.3 },
    { time: "15 Nov", temperature: 29, humidity: 58, rainfall: 0 },
]


const historicalRecords = [
    {
        timestamp: "15 Nov 2026, 10:00 AM",
        temperature: 27.5,
        humidity: 62,
        rainfall: 0.0,
        windSpeed: 12.4,
    },
    {
        timestamp: "15 Nov 2026, 09:00 AM",
        temperature: 26.8,
        humidity: 65,
        rainfall: 0.2,
        windSpeed: 10.8,
    },
    {
        timestamp: "15 Nov 2026, 08:00 AM",
        temperature: 25.9,
        humidity: 68,
        rainfall: 0.0,
        windSpeed: 11.2,
    },
    {
        timestamp: "15 Nov 2026, 07:00 AM",
        temperature: 24.7,
        humidity: 71,
        rainfall: 0.0,
        windSpeed: 9.5,
    },
]

function WeatherHistory() {
    const [dateRange, setDateRange] = useState("7")
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

            {/* Date Range Selector */}
            <section className="rounded-xl border border-gray-200 bg-white p-5">
                <h2 className="mb-3 text-sm font-semibold text-gray-900">
                    Select Date Range
                </h2>

                <div className="flex flex-wrap gap-3">

                    <button
                        onClick={() => setDateRange("7")}
                        className={`rounded-lg px-4 py-2 text-sm font-medium ${
                            dateRange === "7"
                            ? "bg-green-300 text-gray-950"
                            : "border border-gray-200 text-gray-600 hover:bg-gray-50"
                        }`}
                    >
                        Last 7 Days
                    </button>

                    <button
                        onClick={() => setDateRange("30")}
                        className={`rounded-lg px-4 py-2 text-sm font-medium ${
                            dateRange === "30"
                            ? "bg-green-300 text-gray-950"
                            : "border border-gray-200 text-gray-600 hover:bg-gray-50"
                        }`}
                    >
                        Last 30 Days
                    </button>

                    <button
                        onClick={() => setDateRange("custom")}
                        className={`rounded-lg px-4 py-2 text-sm font-medium ${
                            dateRange === "custom"
                            ? "bg-green-300 text-gray-950"
                            : "border border-gray-200 text-gray-600 hover:bg-gray-50"
                        }`}
                    >
                        Custom Range
                    </button>
                </div>

                {dateRange === "custom" && (
                    <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2">

                        <div>
                            <label className="mb-2 block text-sm font-medium text-gray-700">
                                Start Date
                            </label>
                            <input 
                                type="date"
                                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" 
                            />
                        </div>

                        <div>
                            <label className="mb-2 block text-sm font-medium text-gray-700">
                                End Date
                            </label>
                            <input 
                                type="date"
                                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" 
                            />
                        </div>

                    </div>
                )}
            </section>

            {/* Historical Summary */}
            <section>
                <h2 className="mb-4 text-lg font-semibold text-gray-900">
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

                    <div className="rounded-xl border border-gray-200  bg-green-200 p-5">
                        <p className="text-sm text-gray-500">
                            Average Humidity
                        </p>
                        <p className="mt-2 text-2xl font-bold text-gray-900">
                            --%
                        </p>
                    </div>

                    <div className="rounded-xl border border-gray-200  bg-green-200 p-5">
                        <p className="text-sm text-gray-500">
                            Total Rainfall
                        </p>
                        <p className="mt-2 text-2xl font-bold text-gray-900">
                            -- mm
                        </p>
                    </div>

                    <div className="rounded-xl border border-gray-200  bg-green-200 p-5">
                        <p className="text-sm text-gray-500">
                            Maxium Wind Speed
                        </p>
                        <p className="mt-2 text-2xl font-bold text-gray-900">
                            -- km/h
                        </p>
                    </div>
                </div>
            </section>

            {/* Historical Temperature Chart */}
            <section>
                <WeatherChart
                    title="Temperature History"
                    data={historicalData}
                    dataKey="temperature"
                    color="#F97316"
                    unit="°C"
                />
            </section>

            {/* Humidity and Rainfall Charts */}
            <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                <WeatherChart 
                    title="Humidity History"
                    data={historicalData}
                    dataKey="humidity"
                    color="#0EA5E9"
                    unit="%"
                />
                <WeatherChart
                    title="Rainfall History"
                    data={historicalData}
                    dataKey="rainfall"
                    color="#6366F1"
                    unit=" mm"
                />
            </div>

            {/* Historical Records Table. */}
            <section className="rounded-2xl border border-gray-200 bg-green-200 p-5 sm:p-6">

                <div className="mb-5">
                    <h2 className="text-lg font-semibold text-gray-900">
                        Historical Records
                    </h2>

                    <p className="mt-1 text-sm text-gray-500">
                        Previously recorded weather observations.
                    </p>
                </div>

                <div className="overflow-x-auto bg-gray-100 rounded-3xl">

                    <table className="w-full min-w-162.5 text-left text-sm">
                        <thead>
                            <tr className="border-b border-gray-200 text-gray-500">
                                <th className="px-4 py-3 font-medium">Date & Time</th>
                                <th className="px-4 py-3 font-medium">Temperature</th>
                                <th className="px-4 py-3 font-medium">Humidity</th>
                                <th className="px-4 py-3 font-medium">Rainfall</th>
                                <th className="px-4 py-3 font-medium">Wind Speed</th>
                            </tr>
                        </thead>

                        <tbody>
                            {historicalRecords.map((record) => (
                                <tr 
                                key={MediaRecorder.timestamp}
                                className="border-b border-gray-100 hover:bg-gray-50">
                                   <td className="px-4 py-4 font-medium text-gray-900">
                                        {record.timestamp}
                                    </td>

                                    <td className="px-4 py-4 text-gray-700">
                                        {record.temperature.toFixed(1)}°C
                                    </td>

                                    <td className="px-4 py-4 text-gray-700">
                                        {record.humidity}%
                                    </td>

                                    <td className="px-4 py-4 text-gray-700">
                                        {record.rainfall.toFixed(1)} mm
                                    </td>

                                    <td className="px-4 py-4 text-gray-700">
                                        {record.windSpeed.toFixed(1)} km/h
                                    </td> 
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    )
}

export default WeatherHistory