import { useState, useEffect } from 'react'
import {
    Package,
    TrendingUp,
    TrendingDown,
    AlertTriangle,
    DollarSign,
    ShoppingCart,
    BarChart3,
    RefreshCw,
    ArrowUpRight,
    ArrowDownRight,
    Boxes,
    Zap
} from 'lucide-react'
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    BarChart,
    Bar,
    PieChart,
    Pie,
    Cell,
    LineChart,
    Line
} from 'recharts'

// Sample data - in production this would come from API
const salesData = [
    { name: 'Mon', sales: 4000, revenue: 24000 },
    { name: 'Tue', sales: 3000, revenue: 18000 },
    { name: 'Wed', sales: 5000, revenue: 30000 },
    { name: 'Thu', sales: 2780, revenue: 16680 },
    { name: 'Fri', sales: 6890, revenue: 41340 },
    { name: 'Sat', sales: 8390, revenue: 50340 },
    { name: 'Sun', sales: 4490, revenue: 26940 },
]

const categoryData = [
    { name: 'Electronics', value: 45, color: '#6366f1' },
    { name: 'Furniture', value: 20, color: '#8b5cf6' },
    { name: 'Clothing', value: 15, color: '#ec4899' },
    { name: 'Food', value: 12, color: '#10b981' },
    { name: 'Other', value: 8, color: '#f59e0b' },
]

const topProducts = [
    { name: 'Wireless Mouse', sold: 1250, revenue: 125000, trend: 12 },
    { name: 'USB Keyboard', sold: 890, revenue: 133500, trend: 8 },
    { name: 'Monitor Stand', sold: 650, revenue: 162500, trend: -3 },
    { name: 'Webcam HD', sold: 520, revenue: 207800, trend: 15 },
    { name: 'Headphones', sold: 480, revenue: 143900, trend: 5 },
]

const lowStockItems = [
    { name: 'USB Hub', current: 0, threshold: 15, severity: 'critical' },
    { name: 'Headphones', current: 8, threshold: 20, severity: 'high' },
    { name: 'Webcam HD', current: 12, threshold: 15, severity: 'medium' },
]

// KPI Card Component
function KPICard({ title, value, change, changeType, icon: Icon, gradient, description }) {
    const isPositive = changeType === 'positive'

    return (
        <div className={`kpi-card ${gradient}`}>
            <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-xl ${gradient === 'success' ? 'bg-success-100' :
                        gradient === 'warning' ? 'bg-warning-100' :
                            gradient === 'danger' ? 'bg-danger-100' :
                                'bg-primary-100'
                    }`}>
                    <Icon className={`w-6 h-6 ${gradient === 'success' ? 'text-success-600' :
                            gradient === 'warning' ? 'text-warning-600' :
                                gradient === 'danger' ? 'text-danger-600' :
                                    'text-primary-600'
                        }`} />
                </div>
                {change && (
                    <div className={`flex items-center gap-1 text-sm font-medium ${isPositive ? 'text-success-600' : 'text-danger-600'
                        }`}>
                        {isPositive ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                        {change}%
                    </div>
                )}
            </div>
            <h3 className="text-3xl font-bold text-gray-900 mb-1">{value}</h3>
            <p className="text-sm text-gray-500">{title}</p>
            {description && <p className="text-xs text-gray-400 mt-1">{description}</p>}
        </div>
    )
}

function Dashboard() {
    const [loading, setLoading] = useState(true)
    const [summary, setSummary] = useState(null)

    useEffect(() => {
        // Simulate API call
        setTimeout(() => {
            setSummary({
                totalProducts: 1247,
                totalValue: 2456789,
                lowStockCount: 8,
                totalSales: 15420,
                totalRevenue: 4521300
            })
            setLoading(false)
        }, 800)
    }, [])

    if (loading) {
        return (
            <div className="animate-fade-in">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <div className="skeleton h-8 w-48 mb-2" />
                        <div className="skeleton h-4 w-64" />
                    </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="skeleton h-36 rounded-2xl" />
                    ))}
                </div>
            </div>
        )
    }

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="flex flex-col lg:flex-row lg:items-center justify-between mb-8 gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">
                        Welcome to <span className="gradient-text">StockFlow</span>
                    </h1>
                    <p className="text-gray-500 mt-1">
                        Real-time inventory monitoring powered by Data Structures & Algorithms
                    </p>
                </div>
                <div className="flex items-center gap-3">
                    <button className="btn-secondary">
                        <RefreshCw className="w-4 h-4" />
                        Refresh
                    </button>
                    <button className="btn-primary">
                        <Zap className="w-4 h-4" />
                        Process Queue
                    </button>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <KPICard
                    title="Total Products"
                    value={summary.totalProducts.toLocaleString()}
                    change={12}
                    changeType="positive"
                    icon={Package}
                    description="Using HashMap O(1) lookup"
                />
                <KPICard
                    title="Inventory Value"
                    value={`₹${(summary.totalValue / 100000).toFixed(1)}L`}
                    change={8}
                    changeType="positive"
                    icon={DollarSign}
                    gradient="success"
                    description="AVL Tree range queries"
                />
                <KPICard
                    title="Low Stock Alerts"
                    value={summary.lowStockCount}
                    change={-15}
                    changeType="positive"
                    icon={AlertTriangle}
                    gradient="warning"
                    description="Min-Heap priority alerts"
                />
                <KPICard
                    title="Daily Sales"
                    value={summary.totalSales.toLocaleString()}
                    change={23}
                    changeType="positive"
                    icon={ShoppingCart}
                    gradient="success"
                    description="Queue FIFO processing"
                />
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {/* Sales Trend Chart */}
                <div className="lg:col-span-2 chart-container">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">Sales Trend</h3>
                            <p className="text-sm text-gray-500">Last 7 days performance</p>
                        </div>
                        <div className="flex items-center gap-4 text-sm">
                            <span className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-primary-500" />
                                Units Sold
                            </span>
                            <span className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-success-500" />
                                Revenue
                            </span>
                        </div>
                    </div>
                    <ResponsiveContainer width="100%" height={280}>
                        <AreaChart data={salesData}>
                            <defs>
                                <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
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
                                dataKey="sales"
                                stroke="#6366f1"
                                strokeWidth={2}
                                fillOpacity={1}
                                fill="url(#colorSales)"
                            />
                            <Area
                                type="monotone"
                                dataKey="revenue"
                                stroke="#10b981"
                                strokeWidth={2}
                                fillOpacity={1}
                                fill="url(#colorRevenue)"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

                {/* Category Distribution */}
                <div className="chart-container">
                    <div className="mb-6">
                        <h3 className="text-lg font-semibold text-gray-900">Categories</h3>
                        <p className="text-sm text-gray-500">Product distribution</p>
                    </div>
                    <ResponsiveContainer width="100%" height={200}>
                        <PieChart>
                            <Pie
                                data={categoryData}
                                cx="50%"
                                cy="50%"
                                innerRadius={50}
                                outerRadius={80}
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {categoryData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                    <div className="flex flex-wrap gap-2 mt-4">
                        {categoryData.map((cat) => (
                            <span key={cat.name} className="flex items-center gap-1 text-xs text-gray-600">
                                <span className="w-2 h-2 rounded-full" style={{ background: cat.color }} />
                                {cat.name}
                            </span>
                        ))}
                    </div>
                </div>
            </div>

            {/* Bottom Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Top Products */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">Top Sellers</h3>
                            <p className="text-sm text-gray-500">Using Max-Heap for O(log n) extraction</p>
                        </div>
                        <TrendingUp className="w-5 h-5 text-success-500" />
                    </div>
                    <div className="space-y-4">
                        {topProducts.map((product, index) => (
                            <div key={product.name} className="flex items-center gap-4">
                                <span className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-100 to-purple-100 flex items-center justify-center text-sm font-bold text-primary-600">
                                    {index + 1}
                                </span>
                                <div className="flex-1 min-w-0">
                                    <p className="font-medium text-gray-900 truncate">{product.name}</p>
                                    <p className="text-sm text-gray-500">{product.sold.toLocaleString()} units</p>
                                </div>
                                <div className="text-right">
                                    <p className="font-semibold text-gray-900">₹{(product.revenue / 1000).toFixed(0)}K</p>
                                    <p className={`text-xs flex items-center justify-end gap-1 ${product.trend > 0 ? 'text-success-600' : 'text-danger-600'
                                        }`}>
                                        {product.trend > 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                                        {Math.abs(product.trend)}%
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Low Stock Alerts */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">Low Stock Alerts</h3>
                            <p className="text-sm text-gray-500">Priority Queue sorted by urgency</p>
                        </div>
                        <AlertTriangle className="w-5 h-5 text-warning-500" />
                    </div>
                    <div className="space-y-4">
                        {lowStockItems.map((item) => (
                            <div key={item.name} className="flex items-center gap-4 p-3 rounded-xl bg-gray-50">
                                <div className={`w-2 h-full min-h-[40px] rounded-full ${item.severity === 'critical' ? 'bg-danger-500' :
                                        item.severity === 'high' ? 'bg-warning-500' :
                                            'bg-yellow-400'
                                    }`} />
                                <div className="flex-1">
                                    <div className="flex items-center gap-2">
                                        <p className="font-medium text-gray-900">{item.name}</p>
                                        <span className={`badge ${item.severity === 'critical' ? 'badge-danger' :
                                                item.severity === 'high' ? 'badge-warning' :
                                                    'bg-yellow-50 text-yellow-700'
                                            }`}>
                                            {item.severity}
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-2 mt-1">
                                        <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                                            <div
                                                className={`h-full rounded-full ${item.severity === 'critical' ? 'bg-danger-500' :
                                                        item.severity === 'high' ? 'bg-warning-500' :
                                                            'bg-yellow-400'
                                                    }`}
                                                style={{ width: `${(item.current / item.threshold) * 100}%` }}
                                            />
                                        </div>
                                        <span className="text-xs text-gray-500">
                                            {item.current}/{item.threshold}
                                        </span>
                                    </div>
                                </div>
                                <button className="btn-primary text-sm py-1.5 px-3">
                                    Reorder
                                </button>
                            </div>
                        ))}
                    </div>
                    <button className="w-full mt-4 py-3 text-center text-primary-600 font-medium hover:bg-primary-50 rounded-xl transition-colors">
                        View All Alerts →
                    </button>
                </div>
            </div>

            {/* DSA Showcase Footer */}
            <div className="mt-8 p-6 rounded-2xl bg-gradient-to-r from-primary-500 to-purple-600 text-white">
                <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                    <div>
                        <h3 className="text-xl font-bold mb-1">🎓 DSA + Data Science Project</h3>
                        <p className="text-white/80">
                            This system demonstrates HashMap, AVL Tree, Binary Heap, Trie, Graph, and Queue data structures combined with NumPy/Pandas analytics.
                        </p>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="px-4 py-2 rounded-xl bg-white/20 text-sm font-medium">
                            6+ Data Structures
                        </span>
                        <span className="px-4 py-2 rounded-xl bg-white/20 text-sm font-medium">
                            Real-time Analytics
                        </span>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Dashboard
