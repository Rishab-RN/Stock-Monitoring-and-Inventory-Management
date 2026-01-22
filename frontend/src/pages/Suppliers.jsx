import { useState } from 'react'
import { Truck, Plus, Search, MapPin, Clock, Star, Link2 } from 'lucide-react'

const sampleSuppliers = [
    { id: 'SUP001', name: 'Tech Components Ltd', address: 'Mumbai', lead_time_days: 5, reliability_score: 0.95, products: 4 },
    { id: 'SUP002', name: 'Office Furniture Co', address: 'Delhi', lead_time_days: 7, reliability_score: 0.88, products: 3 },
    { id: 'SUP003', name: 'Premium Electronics', address: 'Bangalore', lead_time_days: 3, reliability_score: 0.97, products: 3 },
    { id: 'SUP004', name: 'Home Essentials Hub', address: 'Pune', lead_time_days: 4, reliability_score: 0.91, products: 1 },
]

function Suppliers() {
    const [searchQuery, setSearchQuery] = useState('')
    const filtered = sampleSuppliers.filter(s => s.name.toLowerCase().includes(searchQuery.toLowerCase()))

    return (
        <div className="animate-fade-in">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Supplier Network</h1>
                    <p className="text-gray-500"><span className="text-primary-600 font-medium">Graph</span> - BFS/DFS • Dijkstra</p>
                </div>
                <button className="btn-primary"><Plus className="w-4 h-4" />Add Supplier</button>
            </div>

            <div className="card p-4 mb-6">
                <div className="input-group max-w-md">
                    <Search className="input-icon w-5 h-5" />
                    <input type="text" placeholder="Search suppliers..." className="input-with-icon" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filtered.map((s) => (
                    <div key={s.id} className="card p-5">
                        <div className="flex items-center gap-4 mb-4">
                            <div className="w-12 h-12 rounded-xl gradient-primary flex items-center justify-center text-white font-bold text-lg">{s.name.charAt(0)}</div>
                            <div className="flex-1">
                                <h3 className="font-semibold text-gray-900">{s.name}</h3>
                                <p className="text-sm text-gray-500">{s.id}</p>
                            </div>
                            <span className={`px-3 py-1 rounded-full text-sm font-medium ${s.reliability_score >= 0.95 ? 'badge-success' : 'badge-warning'}`}>
                                <Star className="w-3 h-3 inline mr-1" />{(s.reliability_score * 100).toFixed(0)}%
                            </span>
                        </div>
                        <div className="grid grid-cols-3 gap-4 text-sm text-gray-600">
                            <div className="flex items-center gap-2"><MapPin className="w-4 h-4 text-gray-400" />{s.address}</div>
                            <div className="flex items-center gap-2"><Clock className="w-4 h-4 text-gray-400" />{s.lead_time_days} days</div>
                            <div className="flex items-center gap-2"><Link2 className="w-4 h-4 text-primary-500" />{s.products} products</div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-6 p-6 rounded-2xl bg-gradient-to-r from-primary-500 to-purple-600 text-white">
                <h3 className="text-lg font-bold mb-2">🔗 Graph Algorithms</h3>
                <div className="grid grid-cols-3 gap-4 mt-4 text-sm">
                    <div className="p-3 rounded-lg bg-white/10"><strong>BFS</strong> - Find connected suppliers</div>
                    <div className="p-3 rounded-lg bg-white/10"><strong>Dijkstra</strong> - Shortest lead time</div>
                    <div className="p-3 rounded-lg bg-white/10"><strong>Centrality</strong> - Key suppliers</div>
                </div>
            </div>
        </div>
    )
}

export default Suppliers
