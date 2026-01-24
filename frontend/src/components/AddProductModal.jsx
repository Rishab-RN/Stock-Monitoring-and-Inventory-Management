import { useState } from 'react'
import { X, Package, DollarSign, Layers, Hash } from 'lucide-react'
import { createProduct } from '../services/api'

export default function AddProductModal({ isOpen, onClose, onProductAdded }) {
    const [loading, setLoading] = useState(false)
    const [formData, setFormData] = useState({
        id: '',
        name: '',
        category: 'Electronics',
        quantity: 0,
        price: 0,
        cost: 0,
        threshold: 10
    })

    if (!isOpen) return null

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        try {
            await createProduct(formData)
            onProductAdded()
            onClose()
            // Reset form
            setFormData({
                id: '',
                name: '',
                category: 'Electronics',
                quantity: 0,
                price: 0,
                cost: 0,
                threshold: 10
            })
        } catch (error) {
            console.error("Error creating product:", error)
            const errorMessage = error.response?.data?.detail || 'Failed to create product. Please check your network connection.'
            alert(errorMessage)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-2xl w-full max-w-lg shadow-2xl transform transition-all scale-100">
                <div className="flex justify-between items-center p-6 border-b border-slate-100">
                    <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                        <Package className="w-5 h-5 text-violet-600" />
                        Add New Product
                    </h2>
                    <button onClick={onClose} className="p-2 hover:bg-slate-100 rounded-full transition-colors">
                        <X className="w-5 h-5 text-slate-500" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-1">
                            <label className="text-sm font-semibold text-slate-600">Product ID</label>
                            <div className="relative">
                                <Hash className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                                <input
                                    required
                                    type="text"
                                    placeholder="e.g. PROD099"
                                    className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-violet-500 font-mono text-sm"
                                    value={formData.id}
                                    onChange={e => setFormData({ ...formData, id: e.target.value })}
                                />
                            </div>
                        </div>
                        <div className="space-y-1">
                            <label className="text-sm font-semibold text-slate-600">Category</label>
                            <div className="relative">
                                <Layers className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                                <select
                                    className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-violet-500 text-sm appearance-none"
                                    value={formData.category}
                                    onChange={e => setFormData({ ...formData, category: e.target.value })}
                                >
                                    <option>Electronics</option>
                                    <option>Furniture</option>
                                    <option>Home</option>
                                    <option>Food</option>
                                    <option>Other</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-1">
                        <label className="text-sm font-semibold text-slate-600">Product Name</label>
                        <input
                            required
                            type="text"
                            placeholder="e.g. Wireless Gaming Mouse"
                            className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-violet-500 text-sm"
                            value={formData.name}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                        />
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                        <div className="space-y-1">
                            <label className="text-sm font-semibold text-slate-600">Price (Sell) <span className="text-[10px] text-slate-400 font-normal ml-1">To Customer</span></label>
                            <input
                                required
                                type="number"
                                min="0"
                                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-violet-500 text-sm"
                                value={formData.price}
                                onChange={e => setFormData({ ...formData, price: Number(e.target.value) })}
                            />
                        </div>
                        <div className="space-y-1">
                            <label className="text-sm font-semibold text-slate-600">Cost (Buy) <span className="text-[10px] text-slate-400 font-normal ml-1">From Supplier</span></label>
                            <input
                                required
                                type="number"
                                min="0"
                                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-violet-500 text-sm"
                                value={formData.cost}
                                onChange={e => setFormData({ ...formData, cost: Number(e.target.value) })}
                            />
                        </div>
                        <div className="space-y-1">
                            <label className="text-sm font-semibold text-slate-600">Quantity</label>
                            <input
                                required
                                type="number"
                                min="0"
                                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-violet-500 text-sm"
                                value={formData.quantity}
                                onChange={e => setFormData({ ...formData, quantity: Number(e.target.value) })}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full mt-4 py-3 bg-violet-600 hover:bg-violet-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-violet-200 active:scale-95 disabled:opacity-70 flex items-center justify-center gap-2"
                    >
                        {loading ? 'Adding...' : 'Add Product'}
                    </button>
                </form>
            </div>
        </div>
    )
}
