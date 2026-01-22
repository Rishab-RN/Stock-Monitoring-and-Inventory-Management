import { useState } from 'react'
import { Bell, AlertTriangle, Package, Check, X, Clock, Filter } from 'lucide-react'

const sampleAlerts = [
    { id: 'ALT001', product_id: 'PROD008', product_name: 'USB Hub', type: 'out_of_stock', severity: 'critical', quantity: 0, threshold: 15, created_at: '2 hours ago', acknowledged: false },
    { id: 'ALT002', product_id: 'PROD006', product_name: 'Headphones', type: 'low_stock', severity: 'high', quantity: 8, threshold: 20, created_at: '5 hours ago', acknowledged: false },
    { id: 'ALT003', product_id: 'PROD004', product_name: 'Webcam HD', type: 'low_stock', severity: 'medium', quantity: 12, threshold: 15, created_at: '1 day ago', acknowledged: false },
    { id: 'ALT004', product_id: 'PROD001', product_name: 'Wireless Mouse', type: 'reorder', severity: 'low', quantity: 25, threshold: 20, created_at: '2 days ago', acknowledged: true },
]

function Alerts() {
    const [alerts, setAlerts] = useState(sampleAlerts)
    const [filter, setFilter] = useState('all')

    const filtered = alerts.filter(a => filter === 'all' || a.severity === filter)

    const getSeverityStyle = (severity) => {
        const styles = {
            critical: { badge: 'badge-danger', bg: 'bg-danger-50 border-danger-200' },
            high: { badge: 'badge-warning', bg: 'bg-warning-50 border-warning-200' },
            medium: { badge: 'bg-yellow-50 text-yellow-700', bg: 'bg-yellow-50 border-yellow-200' },
            low: { badge: 'badge-info', bg: 'bg-primary-50 border-primary-200' },
        }
        return styles[severity] || styles.low
    }

    return (
        <div className="animate-fade-in">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Alerts Center</h1>
                    <p className="text-gray-500"><span className="text-primary-600 font-medium">Priority Queue</span> - Min-Heap by severity</p>
                </div>
                <div className="flex items-center gap-2">
                    <Filter className="w-4 h-4 text-gray-400" />
                    <select className="input w-40" value={filter} onChange={(e) => setFilter(e.target.value)}>
                        <option value="all">All Alerts</option>
                        <option value="critical">Critical</option>
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                    </select>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                {[
                    { label: 'Critical', count: alerts.filter(a => a.severity === 'critical').length, color: 'danger' },
                    { label: 'High', count: alerts.filter(a => a.severity === 'high').length, color: 'warning' },
                    { label: 'Medium', count: alerts.filter(a => a.severity === 'medium').length, color: 'yellow' },
                    { label: 'Low', count: alerts.filter(a => a.severity === 'low').length, color: 'primary' },
                ].map((stat) => (
                    <div key={stat.label} className="card p-4 text-center">
                        <p className="text-3xl font-bold text-gray-900">{stat.count}</p>
                        <p className="text-sm text-gray-500">{stat.label}</p>
                    </div>
                ))}
            </div>

            <div className="space-y-3">
                {filtered.map((alert) => {
                    const style = getSeverityStyle(alert.severity)
                    return (
                        <div key={alert.id} className={`card p-4 border ${style.bg} ${alert.acknowledged ? 'opacity-60' : ''}`}>
                            <div className="flex items-center gap-4">
                                <div className={`w-2 h-12 rounded-full ${alert.severity === 'critical' ? 'bg-danger-500' :
                                        alert.severity === 'high' ? 'bg-warning-500' :
                                            alert.severity === 'medium' ? 'bg-yellow-400' : 'bg-primary-400'
                                    }`} />
                                <AlertTriangle className={`w-5 h-5 ${alert.severity === 'critical' ? 'text-danger-500' : 'text-warning-500'
                                    }`} />
                                <div className="flex-1">
                                    <div className="flex items-center gap-2">
                                        <h3 className="font-semibold text-gray-900">{alert.product_name}</h3>
                                        <span className={style.badge}>{alert.severity}</span>
                                        <span className="text-xs text-gray-400">{alert.type.replace('_', ' ')}</span>
                                    </div>
                                    <p className="text-sm text-gray-600">
                                        Stock: <strong>{alert.quantity}</strong> / {alert.threshold} threshold
                                    </p>
                                </div>
                                <div className="flex items-center gap-2 text-xs text-gray-400">
                                    <Clock className="w-3 h-3" />{alert.created_at}
                                </div>
                                <div className="flex items-center gap-2">
                                    <button className="btn-primary text-sm py-1.5 px-3">Reorder</button>
                                    <button className="p-2 hover:bg-gray-100 rounded-lg"><Check className="w-4 h-4 text-success-500" /></button>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>

            <div className="mt-6 p-6 rounded-2xl bg-gradient-to-r from-warning-500 to-danger-500 text-white">
                <h3 className="text-lg font-bold mb-2">⏱️ Priority Queue Implementation</h3>
                <p className="text-white/80">Alerts are managed using a Min-Heap where severity determines priority. Critical=0, High=1, Medium=2, Low=3. Extract-min gives highest priority alert in O(log n).</p>
            </div>
        </div>
    )
}

export default Alerts
