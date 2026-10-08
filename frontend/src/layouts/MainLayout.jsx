import { Outlet } from "react-router-dom"
import Sidebar from "../components/Sidebar"


function MainLayout() {
    return (
        <div className="flex min-h-screen bg-gray-50">
            <Sidebar/>
            <main className="flex-1 min-w-0 p-4 sm:p-6 lg:p-8">
                <Outlet />
            </main>
        </div>
    )
}

export default MainLayout