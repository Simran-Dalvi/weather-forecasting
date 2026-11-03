import axios from "axios"

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 10000,
})

export async function getCurrentWeather() {
    const response = await api.get("/weather/current")
    return response.data
}

export async function getWeatherPrediction() {
    const response = await api.get("/weather/predict")
    return response.data
}

export default api