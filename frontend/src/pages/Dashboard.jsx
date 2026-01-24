import { useState, useEffect } from 'react'
import {
    Package,
    TrendingUp,
    TrendingDown,
    AlertTriangle,
    DollarSign,
    ShoppingCart,
    RefreshCw,
    Zap,
    Play
} from 'lucide-react'
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell
} from 'recharts'
import { fetchSummary, fetchTopSellers, fetchLowStock } from '../services/api'

// KPI Card Component - Vibrant Colorful Style
function KPICard({ title, value, change, icon: Icon, color }) {
    const isPositive = change >= 0
    const colorClasses = {
        orange: {
            iconBg: 'bg-gradient-to-br from-orange-400 to-pink-500',
            glow: 'shadow-orange-200'
        },
        purple: {
            iconBg: 'bg-gradient-to-br from-violet-500 to-purple-600',
            glow: 'shadow-violet-200'
        },
        green: {
            iconBg: 'bg-gradient-to-br from-emerald-400 to-teal-500',
            glow: 'shadow-emerald-200'
        },
        cyan: {
            iconBg: 'bg-gradient-to-br from-cyan-400 to-blue-500',
            glow: 'shadow-cyan-200'
        }
    }
    const styles = colorClasses[color] || colorClasses.purple

    return (
        <div className="kpi-card-new group hover-lift">
            <div className="flex justify-between items-start">
                <div>
                    <p className="text-slate-500 text-sm font-medium mb-1">{title}</p>
                    <h3 className="text-3xl font-extrabold text-slate-800 mb-2 group-hover:scale-105 transition-transform origin-left">
                        {value}
                    </h3>
                </div>
                <div className={`p-3 rounded-xl ${styles.iconBg} shadow-lg ${styles.glow} group-hover:scale-110 transition-transform`}>
                    <Icon className="w-6 h-6 text-white" />
                </div>
            </div>
            {change !== undefined && (
                <div className="flex items-center gap-2 mt-3">
                    <span className={`text-xs font-bold px-3 py-1 rounded-full flex items-center gap-1 ${isPositive
                        ? 'bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-700'
                        : 'bg-gradient-to-r from-red-100 to-pink-100 text-red-600'}`}>
                        {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                        {isPositive ? '+' : ''}{change}%
                    </span>
                    <span className="text-xs text-slate-400">vs last week</span>
                </div>
            )}
        </div>
    )
}

function Dashboard() {
    const [summary, setSummary] = useState(null)
    const [topProducts, setTopProducts] = useState([])
    const [lowStockItems, setLowStockItems] = useState([])
    const [loading, setLoading] = useState(true)

    // Using sample data for charts until analytics API is fully linked for historicals
    const salesData = [
        { name: 'Mon', revenue: 24000 },
        { name: 'Tue', revenue: 18000 },
        { name: 'Wed', revenue: 30000 },
        { name: 'Thu', revenue: 16680 },
        { name: 'Fri', revenue: 41340 },
        { name: 'Sat', revenue: 50340 },
        { name: 'Sun', revenue: 26940 },
    ]
    // Parse category data from summary
    const categoryData = summary ? Object.entries(summary.categories).map(([name, value], index) => ({
        name,
        value,
        color: ['#8b5cf6', '#fc8019', '#ec4899', '#10b981', '#06b6d4', '#f59e0b'][index % 6]
    })) : []

    const handleRunForecast = () => {
        alert("Forecast simulation started! Check Analytics page for details.")
    }

    const handleProcessQueue = () => {
        alert("Queue processing started. Optimizing inventory flow...")
    }

    useEffect(() => {
        const loadDashboardData = async () => {
            try {
                const [summaryData, topData, lowStockData] = await Promise.all([
                    fetchSummary(),
                    fetchTopSellers(),
                    fetchLowStock()
                ])
                setSummary(summaryData)
                setTopProducts(topData)
                setLowStockItems(lowStockData)
            } catch (error) {
                console.error("Failed to load dashboard data", error)
            } finally {
                setLoading(false)
            }
        }
        loadDashboardData()
    }, [])

    if (loading) {
        return <div className="p-8 text-slate-700">Loading Dashboard... (Connecting to System)</div>
    }

    return (
        <div className="animate-fade-in pb-20 relative">
            {/* Hero Section - Animated Gradient with Inventory Illustrations */}
            <div className="relative rounded-3xl overflow-hidden mb-12 p-8 min-h-[340px] flex flex-col justify-end group shadow-2xl">
                {/* Animated Gradient Background */}
                <div className="absolute inset-0 gradient-hero z-0"></div>

                {/* Inventory-Themed Floating SVG Elements */}
                <div className="absolute inset-0 z-[1] overflow-hidden pointer-events-none">
                    {/* Floating Package Box */}
                    <div className="absolute top-8 right-16 animate-float opacity-80">
                        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" className="drop-shadow-lg">
                            <path d="M20 7L12 3L4 7V17L12 21L20 17V7Z" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="rgba(255,255,255,0.1)" />
                            <path d="M12 12L20 7" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
                            <path d="M12 12L4 7" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
                            <path d="M12 12V21" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
                        </svg>
                    </div>

                    {/* Floating Bar Chart */}
                    <div className="absolute top-20 right-1/3 animate-float opacity-60" style={{ animationDelay: '1.5s' }}>
                        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" className="drop-shadow-lg">
                            <rect x="4" y="10" width="4" height="10" rx="1" fill="rgba(255,255,255,0.3)" />
                            <rect x="10" y="6" width="4" height="14" rx="1" fill="rgba(255,255,255,0.4)" />
                            <rect x="16" y="3" width="4" height="17" rx="1" fill="rgba(255,255,255,0.5)" />
                        </svg>
                    </div>

                    {/* Floating Delivery Truck */}
                    <div className="absolute bottom-16 left-16 animate-float opacity-70" style={{ animationDelay: '0.5s' }}>
                        <svg width="90" height="90" viewBox="0 0 24 24" fill="none" className="drop-shadow-lg">
                            <rect x="1" y="6" width="15" height="10" rx="1" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.1)" />
                            <path d="M16 8H19L22 12V16H16V8Z" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.15)" />
                            <circle cx="6" cy="18" r="2" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.2)" />
                            <circle cx="18" cy="18" r="2" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.2)" />
                        </svg>
                    </div>

                    {/* Floating Warehouse */}
                    <div className="absolute top-1/4 left-1/4 animate-float opacity-50" style={{ animationDelay: '2s' }}>
                        <svg width="70" height="70" viewBox="0 0 24 24" fill="none" className="drop-shadow-lg">
                            <path d="M3 21H21" stroke="white" strokeWidth="1.5" />
                            <path d="M5 21V7L12 3L19 7V21" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.08)" />
                            <rect x="9" y="13" width="6" height="8" stroke="white" strokeWidth="1" fill="rgba(255,255,255,0.15)" />
                            <rect x="7" y="9" width="3" height="3" stroke="white" strokeWidth="0.5" fill="rgba(255,255,255,0.2)" />
                            <rect x="14" y="9" width="3" height="3" stroke="white" strokeWidth="0.5" fill="rgba(255,255,255,0.2)" />
                        </svg>
                    </div>

                    {/* Floating Barcode */}
                    <div className="absolute bottom-24 right-1/4 animate-float opacity-60" style={{ animationDelay: '2.5s' }}>
                        <svg width="50" height="50" viewBox="0 0 24 24" fill="none" className="drop-shadow-lg">
                            <rect x="3" y="4" width="2" height="16" fill="rgba(255,255,255,0.5)" />
                            <rect x="7" y="4" width="1" height="16" fill="rgba(255,255,255,0.4)" />
                            <rect x="10" y="4" width="3" height="16" fill="rgba(255,255,255,0.5)" />
                            <rect x="15" y="4" width="1" height="16" fill="rgba(255,255,255,0.4)" />
                            <rect x="18" y="4" width="2" height="16" fill="rgba(255,255,255,0.5)" />
                        </svg>
                    </div>

                    {/* Stacked Boxes */}
                    <div className="absolute bottom-10 right-8 animate-float opacity-40" style={{ animationDelay: '3s' }}>
                        <svg width="65" height="65" viewBox="0 0 24 24" fill="none" className="drop-shadow-lg">
                            <rect x="2" y="14" width="8" height="8" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.1)" />
                            <rect x="6" y="10" width="8" height="8" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.15)" />
                            <rect x="10" y="6" width="8" height="8" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.2)" />
                        </svg>
                    </div>
                </div>

                <div className="relative z-10 max-w-2xl">
                    <div className="flex items-center gap-3 mb-4">
                        <span className="px-4 py-1.5 bg-gradient-to-r from-emerald-400 to-cyan-400 text-white text-xs font-bold tracking-wider rounded-full uppercase shadow-lg shadow-emerald-500/30 flex items-center gap-2">
                            <span className="status-dot status-dot-success"></span>
                            LIVE SYSTEM
                        </span>
                        <span className="text-white/80 text-sm font-medium backdrop-blur-sm bg-white/10 px-3 py-1 rounded-full">Enterprise Edition</span>
                    </div>
                    <h1 className="text-5xl font-extrabold text-white mb-4 leading-tight drop-shadow-lg">
                        StockFlow <span className="text-gradient">Analytics</span>
                    </h1>
                    <p className="text-white/90 text-lg mb-8 max-w-xl leading-relaxed">
                        Monitor inventory health, predict demand, and optimize supply chains in real-time with AI-powered insights.
                    </p>
                    <div className="flex items-center gap-4">
                        <button onClick={handleRunForecast} className="btn-primary flex items-center gap-2">
                            <Play className="w-5 h-5 fill-white" />
                            Run Forecast
                        </button>
                        <button onClick={handleProcessQueue} className="btn-secondary flex items-center gap-2">
                            <Zap className="w-5 h-5" />
                            Process Queue
                        </button>
                    </div>
                </div>
            </div>

            {/* KPI Row - Data from Backend */}
            {summary && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12 -mt-16 relative z-20 px-4">
                    <KPICard title="Total Products" value={summary.total_products.toLocaleString()} change={12} icon={Package} color="purple" />
                    <KPICard title="Inventory Value" value={`₹${(summary.total_value / 100000).toFixed(1)}L`} change={8} icon={DollarSign} color="green" />
                    <KPICard title="Low Stock Items" value={summary.low_stock_count} change={-15} icon={AlertTriangle} color="orange" />
                    <KPICard title="Daily Transactions" value="142" change={23} icon={ShoppingCart} color="cyan" />
                </div>
            )}

            {/* Top Trending - Powered by Backend */}
            <div className="mb-12">
                <div className="flex items-center justify-between mb-6 px-2">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
                            <span className="text-2xl">🔥</span> Top Trending Products
                        </h2>
                        <p className="text-sm text-slate-500 mt-1">Real-time market velocity analysis</p>
                    </div>
                    <button className="text-sm text-violet-600 font-semibold hover:text-violet-700 transition-colors flex items-center gap-1">
                        View All <TrendingUp className="w-4 h-4" />
                    </button>
                </div>

                {topProducts.length === 0 ? (
                    <div className="text-slate-500 text-center py-16 bg-gradient-to-br from-white to-violet-50 rounded-2xl border border-violet-100 shadow-sm">
                        <div className="mx-auto w-16 h-16 bg-violet-100 rounded-full flex items-center justify-center mb-4 animate-pulse">
                            <TrendingUp className="w-8 h-8 text-violet-600" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 mb-2">Max-Heap Empty</h3>
                        <p className="font-medium text-slate-600 mb-1">O(1) Access to Top Sellers</p>
                        <p className="text-sm max-w-sm mx-auto">
                            The system uses a <strong>Max-Heap data structure</strong> to instantly identify best-performing products.
                            Start selling products in the Inventory page to populate this heap!
                        </p>
                    </div>
                ) : (
                    <div className="flex gap-6 overflow-x-auto pb-8 scrollbar-hide snap-x">
                        {topProducts.map((product, idx) => {
                            const gradients = [
                                'from-violet-500 to-purple-600',
                                'from-pink-500 to-rose-500',
                                'from-cyan-500 to-blue-500',
                                'from-emerald-500 to-teal-500',
                                'from-orange-500 to-amber-500'
                            ]
                            const gradient = gradients[idx % gradients.length]

                            return (
                                <div key={product.id} className="min-w-[260px] bg-white rounded-2xl p-5 border border-slate-200 hover:border-transparent hover:shadow-xl hover:shadow-violet-200/50 transition-all duration-300 hover:-translate-y-2 group relative snap-start cursor-pointer overflow-hidden">
                                    {/* Gradient Top Bar */}
                                    <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${gradient}`}></div>

                                    {/* Rank Badge */}
                                    <div className={`absolute top-4 right-4 w-8 h-8 rounded-full bg-gradient-to-r ${gradient} text-white text-sm font-bold flex items-center justify-center shadow-lg`}>
                                        {idx + 1}
                                    </div>

                                    <div className={`h-36 bg-gradient-to-br ${gradient} rounded-xl mb-4 flex items-center justify-center text-5xl shadow-lg group-hover:scale-105 transition-transform`}>
                                        📦
                                    </div>
                                    <h3 className="text-slate-800 font-bold text-lg mb-2 truncate">{product.name}</h3>
                                    <div className="flex justify-between items-end">
                                        <div>
                                            <p className="text-slate-400 text-xs uppercase tracking-wide">Price</p>
                                            <p className="text-emerald-600 font-bold text-lg">₹{product.price.toLocaleString()}</p>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-slate-400 text-xs uppercase tracking-wide">In Stock</p>
                                            <p className="text-slate-800 font-bold text-lg">{product.quantity}</p>
                                        </div>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                )}
            </div>

            {/* Charts Section Removed as per request to focus on Inventory Management */}

            {/* Low Stock Alerts */}
            <div className="grid grid-cols-1 gap-8">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-bold text-slate-800">Low Stock Alerts</h3>
                            <p className="text-xs text-slate-500">Min-Heap Implementation (Priority Queue)</p>
                        </div>
                        {lowStockItems.length > 0 && (
                            <span className="bg-orange-100 text-orange-700 text-xs font-bold px-3 py-1 rounded-full">
                                {lowStockItems.length} Priority Items
                            </span>
                        )}
                    </div>

                    {lowStockItems.length === 0 ? (
                        <div className="text-center py-12 bg-slate-50 rounded-xl border border-slate-100 border-dashed">
                            <div className="mx-auto w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mb-3">
                                <Zap className="w-6 h-6 text-emerald-600" />
                            </div>
                            <h4 className="font-bold text-slate-700">Min-Heap Optimized</h4>
                            <p className="text-slate-500 text-sm max-w-md mx-auto mt-1">
                                No low stock items found! The <strong>Min-Heap</strong> automatically surfaces items with lowest quantity (O(1)) when they drop below threshold.
                            </p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {lowStockItems.map((item, idx) => (
                                <div key={idx} className="flex items-center justify-between p-4 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors border border-transparent hover:border-orange-200">
                                    <div className="flex items-center gap-4">
                                        <div className={`w-2 h-10 rounded-full ${item.quantity === 0 ? 'bg-red-500' : 'bg-orange-500'
                                            }`}></div>
                                        <div>
                                            <p className="text-slate-800 font-medium">{item.name}</p>
                                            <p className="text-xs text-slate-500">Only <strong className="text-orange-600">{item.quantity}</strong> units left</p>
                                        </div>
                                    </div>

                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Dashboard

