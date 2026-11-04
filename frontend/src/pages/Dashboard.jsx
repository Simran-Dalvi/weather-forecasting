import { useEffect, useState } from "react"
import WeatherChart from "../components/WeatherChart"
import {
    getCurrentWeather,
    getWeatherPrediction,
} from "../services/api"

function Dashboard() {
    const [weather, setWeather] = useState(null)
    const [prediction, setPrediction] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] =useState(null)
    useEffect(() => {
        async function fetchWeatherData() {
            try {
                setLoading(true)
                setError(null)

                const [currentData, predictionData] = await Promise.all([
                    getCurrentWeather(),
                    getWeatherPrediction(),
                ])

                setWeather(currentData)
                setPrediction(predictionData)
            } catch(err) {
                console.error("Failed to fetch weather data:", err)
                setError("Unable to load weather data. Please try again.")
            } finally {
                setLoading(false)
            }
        }
        fetchWeatherData()
    }, [])

    if (loading) {
        return <p className="text-gray-500">Loading weather data...</p>
    }

    if (error) {
        return <p className="text-red-500">{error}</p>
    }

    const hourlyRecords = weather?.hourly ?? []
    const latestWeather = hourlyRecords[hourlyRecords.length - 1] ?? null

    const chartData = hourlyRecords.map((record) => ({
        time: new Intl.DateTimeFormat("en-IN", {
            timeZone: "Asia/Kolkata",
            hour:"numeric",
            minute: "2-digit",
            hour12: true,
        }).format(new Date(record.timestamp)),

        temperature: record.temperature,
        humidity: record.humidity,
        rainfall: record.rain,
    }))

    const nextHourPrediction = prediction?.predictions?.[0] ?? null
    const predictedTemperature = nextHourPrediction?.predictions?.temperature
    const predictedTime = nextHourPrediction?.target_time

    const formattedPredictedTime = predictedTime
        ? new Intl.DateTimeFormat("en-IN", {
            timeZone: "Asia/Kolkata",
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
        }).format(new Date(predictedTime))
        : "--"

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
                        {latestWeather?.temperature.toFixed(1)}°C
                    </p>
                </div>
                <div className="rounded-xl border bg-green-200">
                    <p className="text-sm text-gray-500 px-3">
                        Humidity
                    </p>
                    <p className="mt-2 text-2xl font-bold text-gray-900 px-3">
                        {latestWeather?.humidity.toFixed(1)}%
                    </p>
                </div>
                <div className="rounded-xl border bg-green-200">
                    <p className="text-sm text-gray-500 px-3">
                        Rainfall
                    </p>
                    <p className="mt-2 text-2xl font-bold text-gray-900 px-3">
                        {latestWeather?.rain.toFixed(1)} mm
                    </p>
                </div>
                <div className="rounded-xl border bg-green-200">
                    <p className="text-sm text-gray-500 px-3">
                        Wind Speed
                    </p>
                    <p className="mt-2 text-2xl font-bold text-gray-900 px-3">
                        {latestWeather?.wind_speed.toFixed(1)} km/h
                    </p>
                </div>
            </section>

            <section className="rounded-xl border bg-white p-6 sm:p-8">
                <div className="text-center">
                    <p className="text-sm font-medium uppercase tracking-wider text-gray-500">
                        Next-Hour Temperature
                    </p>

                    <p className="mt-4 text-5xl font-bold tracking-tight text-gray-900">
                        {predictedTemperature?.toFixed(1) ?? "--"}°C
                    </p>

                    <p className="mt-2 text-sm text-gray-500">
                        Expected at {formattedPredictedTime}
                    </p>
                </div>
            </section>

            {/* Temperature Chart */}
            <WeatherChart 
                title= "Temperature Trend"
                data={chartData}
                dataKey="temperature"
                color="#F97316"
                unit="°C"
            />

            {/* Humidity and Rainfall Charts */}
            <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                <WeatherChart
                    title="Humidity"
                    data={chartData}
                    dataKey="humidity"
                    color="#0EA5E9"
                    unit="%"
                />

                <WeatherChart
                    title="Rainfall"
                    data={chartData}
                    dataKey="rainfall"
                    color="#6366F1"
                    unit=" mm"
                />
            </div>
        </div>
    )
}

export default Dashboard