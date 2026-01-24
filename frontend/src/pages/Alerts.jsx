import { useState, useEffect } from 'react'
import { AlertTriangle, Check, Clock, Filter } from 'lucide-react'
import { fetchLowStock } from '../services/api'

function Alerts() {
    const [alerts, setAlerts] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadAlerts = async () => {
            try {
                const data = await fetchLowStock()
                const mappedAlerts = data.map((item, index) => ({
                    id: `ALT${index}`,
                    product_name: item.name,
                    severity: item.quantity === 0 ? 'critical' : item.quantity < item.threshold / 2 ? 'high' : 'medium',
                    quantity: item.quantity,
                    threshold: item.threshold,
                    type: 'low_stock',
                    created_at: 'Just now'
                }))
                setAlerts(mappedAlerts)
            } catch (error) {
                console.error("Failed to load alerts", error)
            } finally {
                setLoading(false)
            }
        }
        loadAlerts()
    }, [])

    return (
        <div className="animate-fade-in pb-20 relative">
            {/* Page Header with Alert Decorations */}
            <div className={`relative rounded-2xl overflow-hidden mb-8 p-6 transition-colors duration-500 ${alerts.length > 0
                    ? 'bg-gradient-to-r from-orange-500 via-red-500 to-rose-600'
                    : 'bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-600'
                }`}>
                {/* Floating SVG Decorations */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    {/* Alert Triangle */}
                    <svg className="absolute top-4 right-8 w-20 h-20 opacity-20 animate-float" viewBox="0 0 24 24" fill="none">
                        <path d="M12 2L2 22h20L12 2z" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.1)" />
                        <path d="M12 9v5M12 17v.01" stroke="white" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    {/* Bell */}
                    <svg className="absolute bottom-4 left-1/4 w-14 h-14 opacity-15 animate-float" style={{ animationDelay: '1.5s' }} viewBox="0 0 24 24" fill="none">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.1)" />
                    </svg>
                    {/* Exclamation Circle */}
                    <svg className="absolute top-1/3 left-12 w-12 h-12 opacity-10 animate-float" style={{ animationDelay: '2s' }} viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.08)" />
                        <path d="M12 8v4M12 16v.01" stroke="white" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    {/* Low Stock Box */}
                    <svg className="absolute bottom-6 right-1/4 w-10 h-10 opacity-15 animate-float" style={{ animationDelay: '2.5s' }} viewBox="0 0 24 24" fill="none">
                        <path d="M20 7L12 3L4 7V17L12 21L20 17V7Z" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.1)" />
                        <path d="M8 12h8" stroke="white" strokeWidth="1.5" strokeDasharray="2 2" />
                    </svg>
                </div>

                <div className="relative z-10 flex items-center justify-between">
                    <div>
                        <div className="flex items-center gap-3 mb-2">
                            <span className="text-3xl">{alerts.length > 0 ? '🚨' : '✅'}</span>
                            <h1 className="text-3xl font-bold text-white">Alerts Center</h1>
                        </div>
                        <p className="text-white/80 text-sm">
                            {alerts.length > 0 ? (
                                <>Action required for <span className="bg-white/20 px-2 py-0.5 rounded font-bold">{alerts.length} Low Stock Items</span></>
                            ) : (
                                <>All systems operational. <span className="bg-white/20 px-2 py-0.5 rounded font-bold">Inventory Healthy</span></>
                            )}
                        </p>
                    </div>
                    <div className="flex items-center gap-2">
                        <Filter className="w-4 h-4 text-white/60" />
                        <select className="bg-white/20 backdrop-blur-sm border border-white/30 text-white py-2 px-3 rounded-xl outline-none text-sm">
                            <option value="all">Priority Order</option>
                        </select>
                    </div>
                </div>
            </div>

            {loading ? (
                <div className="text-slate-600">Fetching priority alerts...</div>
            ) : (
                <div className="space-y-4">
                    {alerts.map((alert, idx) => (
                        <div key={idx} className="bg-white border border-slate-200 p-5 rounded-2xl flex items-center gap-5 hover:border-violet-300 transition-colors group shadow-sm">
                            <div className={`w-1.5 h-16 rounded-full ${alert.severity === 'critical' ? 'bg-red-500' : 'bg-orange-500'
                                }`} />

                            <div className={`p-3 rounded-full ${alert.severity === 'critical' ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'
                                }`}>
                                <AlertTriangle className="w-6 h-6" />
                            </div>

                            <div className="flex-1">
                                <div className="flex items-center gap-3 mb-1">
                                    <h3 className="text-lg font-bold text-slate-800 max-w-[200px] truncate">{alert.product_name}</h3>
                                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide ${alert.severity === 'critical' ? 'bg-red-100 text-red-600 border border-red-200' : 'bg-orange-100 text-orange-600 border border-orange-200'
                                        }`}>
                                        {alert.severity} Priority
                                    </span>
                                </div>
                                <p className="text-slate-500 text-sm">
                                    Stock Level: <strong className="text-slate-800">{alert.quantity}</strong> <span className="text-slate-400">/ {alert.threshold} Threshold</span>
                                </p>
                            </div>

                            <div className="hidden md:flex items-center gap-2 text-xs text-slate-400">
                                <Clock className="w-3 h-3" />
                                {alert.created_at}
                            </div>

                            <div className="flex items-center gap-3">
                                <button className="px-4 py-2 bg-violet-600 text-white font-bold text-sm rounded-lg hover:bg-violet-700 transition-colors">
                                    Restock
                                </button>
                                <button className="p-2 rounded-lg bg-slate-100 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 transition-colors">
                                    <Check className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    ))}

                    {alerts.length === 0 && (
                        <div className="text-center py-20 bg-white rounded-2xl border border-slate-200">
                            <Check className="w-12 h-12 text-emerald-500 mx-auto mb-4 opacity-50" />
                            <h3 className="text-xl font-bold text-slate-800">All Clear!</h3>
                            <p className="text-slate-500">No low stock alerts in the Priority Queue.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default Alerts

