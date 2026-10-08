import { NavLink } from "react-router-dom"
import {
    LayoutDashboard,
    CloudSun,
    History,
    Settings,
} from "lucide-react"

const navigation = [
    {
        name: "Dashboard",
        path: "/",
        icon: LayoutDashboard,
    },
    {
        name: "Forecast",
        path: "/forecast",
        icon: CloudSun,
    },
    {
        name: "Weather History",
        path: "/history",
        icon: History,
    },
    {
        name: "System",
        path: "/system",
        icon: Settings,
    }
]

function Sidebar() {
    return (
        <aside className="hidden w-64 min-h-screen shrink-0 border-r bg-white p-4 md:block">
            <div className="mb-8">
                <h1 className="text-xl font-bold">
                    Weather Forecasting
                </h1>

                <p className="text-sm text-gray-500">
                    Weather Intelligence
                </p>
            </div>

            <nav className="space-y-2">
                {navigation.map((item) => {
                    const Icon = item.icon

                    return(
                        <NavLink
                        key={item.path}
                        to={item.path}
                        className={({isActive}) =>
                            `flex item-center gap-3 rounded-lg px-3 py-2 text-sm font-medium ${
                                isActive ? "bg-gray-100 text-gray-900"
                                : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                            }`
                        }
                        >
                            <Icon size={18}/>
                            <span>{item.name}</span>
                        </NavLink>
                    )
                })
            }
            </nav>
        </aside>
    )
}

export default Sidebar