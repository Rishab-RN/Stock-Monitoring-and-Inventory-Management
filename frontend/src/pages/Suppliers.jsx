import { useState, useEffect, useCallback } from 'react'
import {
    Search,
    Plus,
    Filter,
    MapPin,
    Phone,
    Mail,
    Clock,
    Star,
    Truck
} from 'lucide-react'
import api from '../services/api'
import AddSupplierModal from '../components/AddSupplierModal'

function Suppliers() {
    const [suppliers, setSuppliers] = useState([])
    const [searchQuery, setSearchQuery] = useState('')
    const [loading, setLoading] = useState(true)
    const [isAddModalOpen, setIsAddModalOpen] = useState(false)

    const loadSuppliers = useCallback(async () => {
        setLoading(true)
        try {
            const response = await api.get('/suppliers')
            // Handle both array response and object response
            const data = response.data.suppliers || response.data
            setSuppliers(Array.isArray(data) ? data : [])
        } catch (error) {
            console.error("Failed to load suppliers", error)
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        loadSuppliers()
    }, [loadSuppliers])

    const filtered = suppliers.filter(s =>
        s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        s.id.toLowerCase().includes(searchQuery.toLowerCase())
    )

    return (
        <div className="animate-fade-in pb-24 relative">
            <AddSupplierModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onSupplierAdded={loadSuppliers}
            />

            {/* Page Header with Decorative Elements */}
            <div className="relative rounded-2xl overflow-hidden mb-8 p-6 bg-gradient-to-r from-cyan-600 via-teal-600 to-emerald-600">
                {/* Floating SVG Decorations */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    {/* Delivery Truck */}
                    <svg className="absolute top-4 right-8 w-20 h-20 opacity-20 animate-float" viewBox="0 0 24 24" fill="none">
                        <rect x="1" y="6" width="15" height="10" rx="1" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.1)" />
                        <path d="M16 8H19L22 12V16H16V8Z" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.15)" />
                        <circle cx="6" cy="18" r="2" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.2)" />
                        <circle cx="18" cy="18" r="2" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.2)" />
                    </svg>
                    {/* Globe/Network */}
                    <svg className="absolute bottom-4 left-1/4 w-14 h-14 opacity-15 animate-float" style={{ animationDelay: '1.5s' }} viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="white" strokeWidth="1.5" />
                        <path d="M2 12H22M12 2C14.5 4.5 16 8 16 12C16 16 14.5 19.5 12 22M12 2C9.5 4.5 8 8 8 12C8 16 9.5 19.5 12 22" stroke="white" strokeWidth="1" />
                    </svg>
                    {/* Warehouse */}
                    <svg className="absolute top-1/3 left-10 w-12 h-12 opacity-10 animate-float" style={{ animationDelay: '2s' }} viewBox="0 0 24 24" fill="none">
                        <path d="M3 21H21M5 21V7L12 3L19 7V21" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.08)" />
                        <rect x="9" y="13" width="6" height="8" stroke="white" strokeWidth="1" fill="rgba(255,255,255,0.15)" />
                    </svg>
                </div>

                <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                    <div>
                        <div className="flex items-center gap-3 mb-2">
                            <span className="text-3xl">🚚</span>
                            <h1 className="text-3xl font-bold text-white">Supplier Network</h1>
                        </div>
                        <div className="flex items-center gap-2 text-white/80 text-sm">
                            <span className="px-2 py-0.5 rounded bg-white/20 backdrop-blur-sm font-mono text-xs">Total Partners</span>
                            <span className="font-bold">{suppliers.length}</span>
                            <span className="text-white/50">•</span>
                            <span>Supply chain analytics</span>
                        </div>
                    </div>
                    <button
                        onClick={() => setIsAddModalOpen(true)}
                        className="flex items-center gap-2 px-5 py-3 bg-white text-cyan-700 font-bold rounded-xl hover:translate-y-[-2px] hover:shadow-lg transition-all"
                    >
                        <Plus className="w-5 h-5" />
                        Add Supplier
                    </button>
                </div>
            </div>

            <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-2xl mb-8 sticky top-4 z-30">
                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
                    <input
                        type="text"
                        placeholder="Search suppliers..."
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl py-3 pl-12 pr-4 text-slate-800 focus:outline-none focus:border-violet-500 transition-colors"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>
            </div>

            {loading ? (
                <div className="text-center py-20 text-slate-500">Loading supplier network...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filtered.map((s) => (
                        <div key={s.id} className="bg-white border border-slate-200 rounded-2xl p-6 hover:border-violet-300 transition-all group shadow-sm hover:shadow-lg">
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex items-center gap-4">
                                    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-indigo-200">
                                        {s.name.charAt(0)}
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-slate-800 text-lg leading-tight">{s.name}</h3>
                                        <p className="text-sm text-slate-400 font-mono mt-1">{s.id}</p>
                                    </div>
                                </div>
                                <span className={`px-2 py-1 rounded-lg text-xs font-bold flex items-center gap-1 ${s.reliability_score >= 0.95 ? 'bg-emerald-100 text-emerald-600' : 'bg-amber-100 text-amber-600'}`}>
                                    <Star className="w-3 h-3 fill-current" />
                                    {(s.reliability_score * 100).toFixed(0)}%
                                </span>
                            </div>

                            <div className="grid grid-cols-2 gap-4 text-sm mt-6 pt-6 border-t border-slate-100">
                                <div className="flex items-center gap-3 text-slate-500">
                                    <div className="p-2 rounded-lg bg-slate-100">
                                        <MapPin className="w-4 h-4 text-slate-600" />
                                    </div>
                                    {s.address || 'N/A'}
                                </div>
                                <div className="flex items-center gap-3 text-slate-500">
                                    <div className="p-2 rounded-lg bg-slate-100">
                                        <Clock className="w-4 h-4 text-slate-600" />
                                    </div>
                                    {s.lead_time_days} Days
                                </div>
                                <div className="flex items-center gap-3 text-slate-500 col-span-2">
                                    <div className="p-2 rounded-lg bg-slate-100">
                                        <Mail className="w-4 h-4 text-slate-600" />
                                    </div>
                                    {s.contact_email || 'No email provided'}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default Suppliers
