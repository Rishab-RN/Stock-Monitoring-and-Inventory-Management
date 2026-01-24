import { useState, useEffect, useCallback } from 'react'
import {
    Search,
    Plus,
    Filter,
    Edit,
    Trash2,
    Package,
    ArrowUpDown,
    Download,
    Upload,
    LayoutGrid,
    List,
    TrendingUp,
    DollarSign
} from 'lucide-react'
import { fetchProducts, searchProducts, deleteProduct } from '../services/api'
import AddProductModal from '../components/AddProductModal'
import TradeModal from '../components/TradeModal'

// Using random placeholder images for visual appeal since we don't have real product images yet
const getRandomImage = (category) => {
    const images = {
        'Electronics': 'https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=800&q=80',
        'Furniture': 'https://images.unsplash.com/photo-1592078615290-033ee584e267?w=800&q=80',
        'Home': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80',
        'default': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80'
    }
    return images[category] || images['default']
}

function Inventory() {
    const [products, setProducts] = useState([])
    const [searchQuery, setSearchQuery] = useState('')
    const [selectedCategory, setSelectedCategory] = useState('all')
    const [viewMode, setViewMode] = useState('grid')
    const [loading, setLoading] = useState(true)
    const [isAddModalOpen, setIsAddModalOpen] = useState(false)
    const [isTradeModalOpen, setIsTradeModalOpen] = useState(false)
    const [tradeMode, setTradeMode] = useState('buy')
    const [selectedProduct, setSelectedProduct] = useState(null)

    const categories = ['all', 'Electronics', 'Furniture', 'Home', 'Food', 'Other']

    const loadProducts = useCallback(async () => {
        setLoading(true)
        try {
            let data
            if (searchQuery.length > 2) {
                data = await searchProducts(searchQuery)
            } else {
                const params = selectedCategory !== 'all' ? { category: selectedCategory } : {}
                const response = await fetchProducts(params)
                data = response.products
            }
            setProducts(data || [])
        } catch (error) {
            console.error("Failed to load products", error)
        } finally {
            setLoading(false)
        }
    }, [searchQuery, selectedCategory])

    useEffect(() => {
        const timer = setTimeout(loadProducts, 300)
        return () => clearTimeout(timer)
    }, [loadProducts])

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this product?')) return
        try {
            await deleteProduct(id)
            loadProducts() // Reload list
        } catch (error) {
            alert('Failed to delete product')
        }
    }

    const getStockStatus = (product) => {
        if (product.quantity === 0) return { label: 'Out of Stock', color: 'text-red-500' }
        if (product.quantity < product.threshold) return { label: 'Low Stock', color: 'text-orange-500' }
        return { label: 'In Stock', color: 'text-emerald-500' }
    }

    const openTradeModal = (product, mode = 'buy') => {
        setSelectedProduct(product)
        setTradeMode(mode)
        setIsTradeModalOpen(true)
    }

    return (
        <div className="animate-fade-in pb-24 relative">
            <AddProductModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onProductAdded={loadProducts}
            />

            <TradeModal
                isOpen={isTradeModalOpen}
                product={selectedProduct}
                initialMode={tradeMode}
                onClose={() => setIsTradeModalOpen(false)}
                onTransactionComplete={loadProducts}
            />

            {/* Page Header with Decorative Elements */}
            <div className="relative rounded-2xl overflow-hidden mb-8 p-6 bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600">
                {/* Floating SVG Decorations */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <svg className="absolute top-4 right-8 w-16 h-16 opacity-20 animate-float" viewBox="0 0 24 24" fill="none">
                        <path d="M20 7L12 3L4 7V17L12 21L20 17V7Z" stroke="white" strokeWidth="1.5" fill="rgba(255,255,255,0.1)" />
                        <path d="M12 12L20 7M12 12L4 7M12 12V21" stroke="white" strokeWidth="1.5" />
                    </svg>
                    <svg className="absolute bottom-4 left-1/3 w-12 h-12 opacity-15 animate-float" style={{ animationDelay: '1s' }} viewBox="0 0 24 24" fill="none">
                        <rect x="4" y="10" width="4" height="10" rx="1" fill="rgba(255,255,255,0.4)" />
                        <rect x="10" y="6" width="4" height="14" rx="1" fill="rgba(255,255,255,0.5)" />
                        <rect x="16" y="3" width="4" height="17" rx="1" fill="rgba(255,255,255,0.6)" />
                    </svg>
                    <svg className="absolute top-1/2 right-1/4 w-10 h-10 opacity-10 animate-float" style={{ animationDelay: '2s' }} viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="4" width="2" height="16" fill="white" />
                        <rect x="7" y="4" width="1" height="16" fill="white" />
                        <rect x="10" y="4" width="3" height="16" fill="white" />
                        <rect x="15" y="4" width="1" height="16" fill="white" />
                        <rect x="18" y="4" width="2" height="16" fill="white" />
                    </svg>
                </div>

                <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                    <div>
                        <div className="flex items-center gap-3 mb-2">
                            <span className="text-3xl">📦</span>
                            <h1 className="text-3xl font-bold text-white">Inventory Management</h1>
                        </div>
                        <div className="flex items-center gap-2 text-white/80 text-sm">
                            <span className="px-2 py-0.5 rounded bg-white/20 backdrop-blur-sm font-mono text-xs">Total Items</span>
                            <span className="font-bold">{products.length || 0}</span>
                            <span className="text-white/50">•</span>
                            <span>Manage your stock efficiently</span>
                        </div>
                    </div>
                    <button
                        onClick={() => setIsAddModalOpen(true)}
                        className="flex items-center gap-2 px-5 py-3 bg-white text-violet-700 font-bold rounded-xl hover:translate-y-[-2px] hover:shadow-lg transition-all"
                    >
                        <Plus className="w-5 h-5" />
                        Add Product
                    </button>
                </div>
            </div>

            {/* Controls Bar */}
            <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-2xl mb-8 flex flex-col md:flex-row gap-4 items-center justify-between sticky top-4 z-30">
                <div className="flex-1 w-full md:w-auto relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
                    <input
                        type="text"
                        placeholder="Search products..."
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl py-3 pl-12 pr-4 text-slate-800 focus:outline-none focus:border-violet-500 transition-colors"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>

                <div className="flex items-center gap-3 w-full md:w-auto">
                    <select
                        className="bg-slate-50 border border-slate-200 text-slate-700 py-3 px-4 rounded-xl outline-none focus:border-violet-500"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        {categories.map(cat => (
                            <option key={cat} value={cat} className="bg-white">
                                {cat === 'all' ? 'All Categories' : cat}
                            </option>
                        ))}
                    </select>

                    <div className="flex bg-slate-100 border border-slate-200 rounded-xl p-1">
                        <button
                            onClick={() => setViewMode('grid')}
                            className={`p-2 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-white text-violet-600 shadow-sm' : 'text-slate-400 hover:text-slate-700'}`}
                        >
                            <LayoutGrid className="w-5 h-5" />
                        </button>
                        <button
                            onClick={() => setViewMode('table')}
                            className={`p-2 rounded-lg transition-all ${viewMode === 'table' ? 'bg-white text-violet-600 shadow-sm' : 'text-slate-400 hover:text-slate-700'}`}
                        >
                            <List className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>

            {loading ? (
                <div className="text-slate-600 text-center py-20">Loading inventory records...</div>
            ) : (
                <>
                    {/* Grid View */}
                    {/* Grid View */}
                    {viewMode === 'grid' && (
                        <>
                            {products.length === 0 ? (
                                <div className="col-span-full py-20 text-center">
                                    <div className="mx-auto w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                                        <Package className="w-10 h-10 text-slate-300" />
                                    </div>
                                    <h3 className="text-xl font-bold text-slate-700 mb-2">No Products Found</h3>
                                    <p className="text-slate-500 max-w-md mx-auto mb-6">
                                        Your inventory is empty. Add a product to get started!
                                    </p>
                                    <button
                                        onClick={() => setIsAddModalOpen(true)}
                                        className="px-6 py-2 bg-violet-600 text-white font-bold rounded-xl hover:bg-violet-700 transition-colors shadow-lg shadow-violet-200"
                                    >
                                        Add First Product
                                    </button>
                                </div>
                            ) : (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                    {products.map(product => {
                                        const status = getStockStatus(product)
                                        const image = getRandomImage(product.category)
                                        return (
                                            <div key={product.id} className="bg-white border border-slate-200 rounded-2xl overflow-hidden hover:border-violet-300 hover:translate-y-[-4px] transition-all duration-300 group shadow-sm hover:shadow-lg">
                                                <div className="h-48 overflow-hidden relative">
                                                    <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 via-transparent to-transparent z-10" />
                                                    <img
                                                        src={image}
                                                        alt={product.name}
                                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                                    />
                                                    <span className={`absolute top-4 right-4 z-20 px-3 py-1 text-xs font-bold rounded-full backdrop-blur-md bg-white/80 text-slate-900 shadow-sm`}>
                                                        {product.category}
                                                    </span>
                                                    <div className="absolute bottom-4 left-4 z-20 text-white">
                                                        <h3 className="text-xl font-bold leading-tight shadow-black drop-shadow-md">{product.name}</h3>
                                                        <p className="font-mono text-white/80 text-xs shadow-black drop-shadow-md">{product.id}</p>
                                                    </div>
                                                </div>
                                                <div className="p-5">
                                                    <div className="flex items-center justify-between mb-6">
                                                        <div>
                                                            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider mb-0.5">Price</p>
                                                            <p className="text-2xl font-black text-slate-800">₹{product.price.toLocaleString()}</p>
                                                        </div>
                                                        <div className="text-right">
                                                            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider mb-0.5">Available</p>
                                                            <p className={`text-lg font-bold ${status.color}`}>
                                                                {product.quantity} <span className="text-xs font-normal text-slate-400">units</span>
                                                            </p>
                                                        </div>
                                                    </div>

                                                    <div className="flex items-center gap-2">
                                                        <button
                                                            onClick={() => openTradeModal(product, 'buy')}
                                                            className="flex-1 py-3 rounded-xl bg-emerald-600 text-white font-bold text-sm hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2 shadow-sm shadow-emerald-200"
                                                        >
                                                            <TrendingUp className="w-4 h-4" /> Restock
                                                        </button>
                                                        <button
                                                            onClick={() => openTradeModal(product, 'sell')}
                                                            className="flex-1 py-3 rounded-xl bg-violet-600 text-white font-bold text-sm hover:bg-violet-700 transition-colors flex items-center justify-center gap-2 shadow-sm shadow-violet-200"
                                                        >
                                                            <DollarSign className="w-4 h-4" /> Sell
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    })}
                                </div>
                            )}
                        </>
                    )}

                    {/* Table View */}
                    {viewMode === 'table' && (
                        <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
                            <table className="w-full min-w-[800px] text-left">
                                <thead className="bg-slate-50 text-slate-500 text-xs uppercase font-semibold">
                                    <tr>
                                        <th className="p-4">Product Details</th>
                                        <th className="p-4">Category</th>
                                        <th className="p-4 text-center">Stock</th>
                                        <th className="p-4 text-right">Price</th>
                                        <th className="p-4 text-center">Status</th>
                                        <th className="p-4 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {products.map(product => {
                                        const status = getStockStatus(product)
                                        return (
                                            <tr key={product.id} className="hover:bg-slate-50 transition-colors group">
                                                <td className="p-4">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center">
                                                            <Package className="w-5 h-5 text-slate-400" />
                                                        </div>
                                                        <div>
                                                            <p className="text-slate-800 font-medium">{product.name}</p>
                                                            <p className="text-slate-400 text-xs font-mono">{product.sku}</p>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td className="p-4">
                                                    <span className="px-2 py-1 bg-slate-100 rounded text-slate-600 text-xs">
                                                        {product.category}
                                                    </span>
                                                </td>
                                                <td className="p-4 text-center">
                                                    <span className="text-slate-800 font-bold">{product.quantity}</span>
                                                    <span className="text-slate-400 text-xs ml-1">/ {product.threshold}</span>
                                                </td>
                                                <td className="p-4 text-right text-slate-600">₹{product.price.toLocaleString()}</td>
                                                <td className="p-4 text-center">
                                                    <span className={`px-2 py-1 rounded text-xs font-bold ${status.color} ${status.bg}`}>
                                                        {status.label}
                                                    </span>
                                                </td>
                                                <td className="p-4 text-right">
                                                    <div className="flex items-center justify-end gap-2">
                                                        <button
                                                            onClick={() => openTradeModal(product, 'buy')}
                                                            title="Restock"
                                                            className="p-2 bg-emerald-100 text-emerald-600 rounded-lg hover:bg-emerald-200 transition-colors"
                                                        >
                                                            <TrendingUp className="w-4 h-4" />
                                                        </button>
                                                        <button
                                                            onClick={() => openTradeModal(product, 'sell')}
                                                            title="Sell"
                                                            className="p-2 bg-violet-100 text-violet-600 rounded-lg hover:bg-violet-200 transition-colors"
                                                        >
                                                            <DollarSign className="w-4 h-4" />
                                                        </button>
                                                        <button
                                                            onClick={() => handleDelete(product.id)}
                                                            title="Delete"
                                                            className="p-2 bg-slate-100 text-slate-400 rounded-lg hover:bg-red-100 hover:text-red-500 transition-colors"
                                                        >
                                                            <Trash2 className="w-4 h-4" />
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                        )
                                    })}
                                </tbody>
                            </table>
                        </div>
                    )}
                </>
            )}
        </div>
    )
}

export default Inventory

