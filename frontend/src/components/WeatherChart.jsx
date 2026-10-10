import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts"

function WeatherChart({
    title,
    data,
    dataKey,
    color,
    unit,
}) {
    return (
        <section className="min-w-0 rounded-2xl border border-gray-200 bg-white p-5 sm:p-6">
            <h2 className="text-base font-semibold text-gray-900">
                {title}
            </h2>

            <div className="mt-5 h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                    data={data}
                    margin={{top:10, right: 16, left: 8, bottom:5}}
                    >
                        <CartesianGrid 
                            strokeDasharray="3 3"
                            vertical={false}
                            stroke="#E5E7EB"
                        />

                        <XAxis 
                            dataKey="time"
                            tick={{fontSize:12, fill: "#6B7280"}}
                            tickLine={false}
                            axisLine={false}
                            tickMargin={10} 
                        />

                        <YAxis
                            tick={{fontSize:12, fill: "#6B7280"}}
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            width={55}
                            tickFormatter={(value) => `${value}${unit}`}
                            domain={["auto", "auto"]} 
                        />

                        <Tooltip
                            labelFormatter={(label) => `Time: ${label}`}
                            formatter={(value) => [
                                `${value}${unit}`,
                                title,
                            ]}
                            contentStyle={{
                                borderRadius: "12px",
                                border: "1px solid #E5E7EB",
                                fontSize: "13px",
                            }} 
                        />

                        <Line
                            type="monotone"
                            dataKey={dataKey}
                            name={title}
                            stroke={color}
                            strokeWidth={2}
                            dot={{
                                r: 2,
                                fill: color,
                                strokeWidth: 0,
                            }}
                            activeDot={{
                                r: 4,
                                fill: color,
                                stroke: "#FFFFFF",
                                strokeWidth: 2,
                            }}
                            connectNulls={false}
                            isAnimationActive={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </section>
    )
}

export default WeatherChart