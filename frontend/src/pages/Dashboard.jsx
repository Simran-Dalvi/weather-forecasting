import WeatherChart from "../components/WeatherChart"

const temperatureData = [
    { time: "12 PM", temperature: 29 },
    { time: "1 PM", temperature: 30 },
    { time: "2 PM", temperature: 31 },
    { time: "3 PM", temperature: 30 },
    { time: "4 PM", temperature: 29 },
    { time: "5 PM", temperature: 28 },
]

const humidityData = [
  { time: "12 PM", humidity: 65 },
  { time: "1 PM", humidity: 62 },
  { time: "2 PM", humidity: 60 },
  { time: "3 PM", humidity: 64 },
  { time: "4 PM", humidity: 68 },
  { time: "5 PM", humidity: 72 },
]

const rainfallData = [
  { time: "12 PM", rainfall: 0 },
  { time: "1 PM", rainfall: 0 },
  { time: "2 PM", rainfall: 0.2 },
  { time: "3 PM", rainfall: 0 },
  { time: "4 PM", rainfall: 0 },
  { time: "5 PM", rainfall: 0 },
]

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

            {/* Temperature Chart */}
            <WeatherChart 
                title= "Temperature Trend"
                data={temperatureData}
                dataKey="temperature"
                color="#F97316"
                unit="°C"
            />

            {/* Humidity and Rainfall Charts */}
            <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                <WeatherChart
                    title="Humidity"
                    data={humidityData}
                    dataKey="humidity"
                    color="#0EA5E9"
                    unit="%"
                />

                <WeatherChart
                    title="Rainfall"
                    data={rainfallData}
                    dataKey="rainfall"
                    color="#6366F1"
                    unit=" mm"
                />
            </div>
        </div>
    )
}

export default Dashboard