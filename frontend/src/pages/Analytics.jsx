import { useState, useEffect } from 'react'
import {
    TrendingUp,
    TrendingDown,
    BarChart3,
    Activity,
    Target,
    Calendar,
    RefreshCw
} from 'lucide-react'
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area,
    BarChart,
    Bar,
    Legend,
    ComposedChart
} from 'recharts'

// Sample forecast data
const forecastData = [
    { name: 'Week 1', actual: 4200, forecast: null, lower: null, upper: null },
    { name: 'Week 2', actual: 3800, forecast: null, lower: null, upper: null },
    { name: 'Week 3', actual: 5100, forecast: null, lower: null, upper: null },
    { name: 'Week 4', actual: 4600, forecast: null, lower: null, upper: null },
    { name: 'Week 5', actual: null, forecast: 4900, lower: 4400, upper: 5400 },
    { name: 'Week 6', actual: null, forecast: 5200, lower: 4600, upper: 5800 },
    { name: 'Week 7', actual: null, forecast: 5500, lower: 4800, upper: 6200 },
    { name: 'Week 8', actual: null, forecast: 5800, lower: 5000, upper: 6600 },
]

const weeklyPattern = [
    { day: 'Mon', sales: 3200 },
    { day: 'Tue', sales: 2800 },
    { day: 'Wed', sales: 3800 },
    { day: 'Thu', sales: 3100 },
    { day: 'Fri', sales: 4500 },
    { day: 'Sat', sales: 5200 },
    { day: 'Sun', sales: 2900 },
]

const trendInsights = [
    { icon: TrendingUp, title: 'Strong Upward Trend', description: 'Sales increasing by 12% week-over-week', type: 'positive' },
    { icon: Activity, title: 'Low Volatility', description: 'Demand is predictable with 15% CV', type: 'info' },
    { icon: Target, title: 'Reorder Recommendation', description: 'Suggested reorder: 450 units for Wireless Mouse', type: 'warning' },
]

function Analytics() {
    const [selectedProduct, setSelectedProduct] = useState('all')
    const [forecastPeriod, setForecastPeriod] = useState(30)
    const [loading, setLoading] = useState(false)

    const products = [
        { id: 'all', name: 'All Products' },
        { id: 'PROD001', name: 'Wireless Mouse' },
        { id: 'PROD002', name: 'USB Keyboard' },
        { id: 'PROD003', name: 'Monitor Stand' },
        { id: 'PROD004', name: 'Webcam HD' },
    ]

    const runForecast = () => {
        setLoading(true)
        setTimeout(() => setLoading(false), 1500)
    }

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="flex flex-col lg:flex-row lg:items-center justify-between mb-6 gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Analytics & Forecasting</h1>
                    <p className="text-gray-500">
                        Time series analysis using <span className="text-primary-600 font-medium">NumPy</span> •
                        Visualization with <span className="text-primary-600 font-medium">Matplotlib</span>
                    </p>
                </div>
                <div className="flex items-center gap-3">
                    <select
                        className="input w-48"
                        value={selectedProduct}
                        onChange={(e) => setSelectedProduct(e.target.value)}
                    >
                        {products.map(p => (
                            <option key={p.id} value={p.id}>{p.name}</option>
                        ))}
                    </select>
                    <button className="btn-primary" onClick={runForecast} disabled={loading}>
                        {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <BarChart3 className="w-4 h-4" />}
                        Run Forecast
                    </button>
                </div>
            </div>

            {/* Analytics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <div className="card p-4">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-primary-100">
                            <TrendingUp className="w-5 h-5 text-primary-600" />
                        </div>
                        <span className="text-sm text-gray-500">Trend Direction</span>
                    </div>
                    <p className="text-2xl font-bold text-success-600">Increasing</p>
                    <p className="text-xs text-gray-400 mt-1">+12.5% growth rate</p>
                </div>

                <div className="card p-4">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-success-100">
                            <Target className="w-5 h-5 text-success-600" />
                        </div>
                        <span className="text-sm text-gray-500">Forecast Accuracy</span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900">94.2%</p>
                    <p className="text-xs text-gray-400 mt-1">MAE: 127 units</p>
                </div>

                <div className="card p-4">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-purple-100">
                            <Calendar className="w-5 h-5 text-purple-600" />
                        </div>
                        <span className="text-sm text-gray-500">Seasonality</span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900">Weekly</p>
                    <p className="text-xs text-gray-400 mt-1">Peak on Saturdays</p>
                </div>

                <div className="card p-4">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-warning-100">
                            <Activity className="w-5 h-5 text-warning-600" />
                        </div>
                        <span className="text-sm text-gray-500">Volatility</span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900">15%</p>
                    <p className="text-xs text-gray-400 mt-1">Low - Predictable demand</p>
                </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                {/* Demand Forecast Chart */}
                <div className="lg:col-span-2 chart-container">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">Demand Forecast</h3>
                            <p className="text-sm text-gray-500">
                                Using <strong>Exponential Moving Average</strong> (EMA) method
                            </p>
                        </div>
                        <div className="flex items-center gap-4 text-sm">
                            <span className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-primary-500" />
                                Actual
                            </span>
                            <span className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-success-500" />
                                Forecast
                            </span>
                        </div>
                    </div>
                    <ResponsiveContainer width="100%" height={300}>
                        <ComposedChart data={forecastData}>
                            <defs>
                                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                            <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                            <YAxis stroke="#94a3b8" fontSize={12} />
                            <Tooltip
                                contentStyle={{
                                    background: 'white',
                                    border: 'none',
                                    borderRadius: '12px',
                                    boxShadow: '0 4px 20px -4px rgba(0,0,0,0.1)'
                                }}
                            />
                            <Area
                                type="monotone"
                                dataKey="upper"
                                fill="#10b98120"
                                stroke="none"
                            />
                            <Area
                                type="monotone"
                                dataKey="lower"
                                fill="white"
                                stroke="none"
                            />
                            <Line
                                type="monotone"
                                dataKey="actual"
                                stroke="#6366f1"
                                strokeWidth={3}
                                dot={{ fill: '#6366f1', strokeWidth: 2, r: 5 }}
                            />
                            <Line
                                type="monotone"
                                dataKey="forecast"
                                stroke="#10b981"
                                strokeWidth={3}
                                strokeDasharray="8 4"
                                dot={{ fill: '#10b981', strokeWidth: 2, r: 5 }}
                            />
                        </ComposedChart>
                    </ResponsiveContainer>
                    <p className="text-xs text-gray-400 mt-4 text-center">
                        Shaded area represents 95% confidence interval
                    </p>
                </div>

                {/* Weekly Pattern */}
                <div className="chart-container">
                    <div className="mb-6">
                        <h3 className="text-lg font-semibold text-gray-900">Weekly Pattern</h3>
                        <p className="text-sm text-gray-500">Average sales by day</p>
                    </div>
                    <ResponsiveContainer width="100%" height={280}>
                        <BarChart data={weeklyPattern}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                            <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} />
                            <YAxis stroke="#94a3b8" fontSize={12} />
                            <Tooltip />
                            <Bar dataKey="sales" fill="url(#barGradient)" radius={[4, 4, 0, 0]}>
                                <defs>
                                    <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%" stopColor="#6366f1" />
                                        <stop offset="100%" stopColor="#8b5cf6" />
                                    </linearGradient>
                                </defs>
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Insights Section */}
            <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 AI-Powered Insights</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {trendInsights.map((insight, index) => (
                        <div
                            key={index}
                            className={`p-4 rounded-xl border ${insight.type === 'positive' ? 'bg-success-50 border-success-200' :
                                    insight.type === 'warning' ? 'bg-warning-50 border-warning-200' :
                                        'bg-primary-50 border-primary-200'
                                }`}
                        >
                            <div className="flex items-center gap-3 mb-2">
                                <insight.icon className={`w-5 h-5 ${insight.type === 'positive' ? 'text-success-600' :
                                        insight.type === 'warning' ? 'text-warning-600' :
                                            'text-primary-600'
                                    }`} />
                                <h4 className="font-medium text-gray-900">{insight.title}</h4>
                            </div>
                            <p className="text-sm text-gray-600">{insight.description}</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Algorithm Info */}
            <div className="mt-6 p-6 rounded-2xl bg-gradient-to-r from-gray-800 to-gray-900 text-white">
                <h3 className="text-lg font-bold mb-4">🧮 Forecasting Algorithms Used</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 rounded-xl bg-white/10">
                        <h4 className="font-semibold mb-2">Simple Moving Average</h4>
                        <p className="text-sm text-gray-300">Window-based averaging for trend smoothing</p>
                        <code className="text-xs text-primary-300 mt-2 block">O(n) time complexity</code>
                    </div>
                    <div className="p-4 rounded-xl bg-white/10">
                        <h4 className="font-semibold mb-2">Exponential Moving Average</h4>
                        <p className="text-sm text-gray-300">Weighted recent values for responsiveness</p>
                        <code className="text-xs text-primary-300 mt-2 block">α = 0.3 smoothing factor</code>
                    </div>
                    <div className="p-4 rounded-xl bg-white/10">
                        <h4 className="font-semibold mb-2">Linear Regression</h4>
                        <p className="text-sm text-gray-300">Trend projection using least squares</p>
                        <code className="text-xs text-primary-300 mt-2 block">R² = 0.89 fit score</code>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Analytics
