import { BrowserRouter, Routes, Route } from "react-router-dom"

import Dashboard from "./pages/Dashboard"
import Forecast from "./pages/Forecast"
import WeatherHistory from "./pages/WeatherHistory"
import System from "./pages/System"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard/>} />
        <Route path="/forecast" element={<Forecast/>} />
        <Route path="/history" element={<WeatherHistory/>} />
        <Route path="/system" element={<System/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App