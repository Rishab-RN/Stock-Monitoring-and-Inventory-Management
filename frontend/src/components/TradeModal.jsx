import { useState, useEffect } from 'react'
import { X, TrendingUp, TrendingDown, DollarSign, Package, Activity } from 'lucide-react'
import { createTransaction, processTransactions } from '../services/api'

export default function TradeModal({ isOpen, onClose, product, onTransactionComplete, initialMode = 'buy' }) {
    // Mode: 'buy' (restock) or 'sell' (sale)
    const [mode, setMode] = useState(initialMode)
    const [quantity, setQuantity] = useState(1)
    const [loading, setLoading] = useState(false)
    const [price, setPrice] = useState(0)

    useEffect(() => {
        if (product) {
            setPrice(product.price)
            setQuantity(1)
            setMode(initialMode)
        }
    }, [product, initialMode])

    if (!isOpen || !product) return null

    // For sales, use current selling price. For restock, use cost price (if available) or 70% of current price as estimate
    const unitPrice = mode === 'sell' ? product.price : (product.cost || product.price * 0.7)
    const totalValue = quantity * unitPrice

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)

        try {
            await createTransaction({
                product_id: product.id,
                transaction_type: mode === 'buy' ? 'restock' : 'sale',
                quantity: parseInt(quantity),
                unit_price: mode === 'buy' ? product.cost : product.price // Logic handled by backend mostly, but sending explicit
            })

            // Process transaction immediately so UI updates
            await processTransactions()

            // Show success animation or toast if we had one
            onTransactionComplete()
            onClose()
        } catch (error) {
            console.error("Transaction failed:", error)
            alert(error.response?.data?.detail || "Transaction failed")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden transform transition-all scale-100">

                {/* Header with Stock Ticker Vibe */}
                <div className="bg-slate-900 p-6 text-white relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <Activity size={100} />
                    </div>

                    <button onClick={onClose} className="absolute top-4 right-4 p-2 bg-white/10 hover:bg-white/20 rounded-full transition-colors z-10">
                        <X className="w-5 h-5 text-white" />
                    </button>

                    <div className="relative z-10">
                        <div className="flex items-center gap-2 mb-1 opacity-80 text-sm font-mono">
                            {product.id} • {product.category}
                        </div>
                        <h2 className="text-2xl font-bold mb-4">{product.name}</h2>

                        <div className="flex items-end gap-3">
                            <span className="text-3xl font-bold">₹{product.price.toLocaleString()}</span>
                            <span className={`flex items-center text-sm font-bold mb-1.5 ${product.velocity >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                {product.velocity > 0 ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                                {Math.abs(product.velocity)} vel
                            </span>
                        </div>
                    </div>
                </div>

                <div className="p-6">
                    {/* Buy/Sell/Switch */}
                    <div className="flex bg-slate-100 p-1 rounded-xl mb-6">
                        <button
                            type="button"
                            onClick={() => setMode('buy')}
                            className={`flex-1 py-2 rounded-lg font-bold text-sm transition-all flex items-center justify-center gap-2 ${mode === 'buy'
                                ? 'bg-white text-emerald-600 shadow-sm'
                                : 'text-slate-500 hover:text-slate-700'
                                }`}
                        >
                            <TrendingUp className="w-4 h-4" /> Buy Stock
                        </button>
                        <button
                            type="button"
                            onClick={() => setMode('sell')}
                            className={`flex-1 py-2 rounded-lg font-bold text-sm transition-all flex items-center justify-center gap-2 ${mode === 'sell'
                                ? 'bg-white text-rose-600 shadow-sm'
                                : 'text-slate-500 hover:text-slate-700'
                                }`}
                        >
                            <TrendingDown className="w-4 h-4" /> Sell Stock
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-sm font-bold text-slate-700 flex justify-between">
                                Quantity
                                <span className={`text-xs font-normal ${product.quantity < 10 ? 'text-rose-500 font-bold' : 'text-slate-500'}`}>
                                    Current Stock: {product.quantity} units
                                </span>
                            </label>
                            <div className="relative">
                                <Package className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                                <input
                                    type="number"
                                    min="1"
                                    max={mode === 'sell' ? product.quantity : 1000}
                                    required
                                    value={quantity}
                                    onChange={(e) => setQuantity(Number(e.target.value))}
                                    className="w-full pl-12 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-violet-500 text-lg font-bold text-slate-800"
                                />
                            </div>
                        </div>

                        {/* Order Summary */}
                        <div className="bg-slate-50 rounded-xl p-4 border border-slate-100 space-y-2">
                            <div className="flex justify-between text-sm text-slate-500">
                                <span>Est. Price / Unit</span>
                                <span>₹{unitPrice.toLocaleString()}</span>
                            </div>
                            <div className="border-t border-slate-200 pt-2 flex justify-between items-center">
                                <span className="font-bold text-slate-800">Total Value</span>
                                <span className="text-xl font-black text-slate-900">₹{totalValue.toLocaleString()}</span>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading || (mode === 'sell' && quantity > product.quantity)}
                            className={`w-full py-4 text-white font-bold text-lg rounded-xl transition-all shadow-lg active:scale-95 flex items-center justify-center gap-2 ${mode === 'buy'
                                ? 'bg-emerald-600 hover:bg-emerald-700 shadow-emerald-200'
                                : 'bg-rose-600 hover:bg-rose-700 shadow-rose-200'
                                } disabled:opacity-50 disabled:cursor-not-allowed`}
                        >
                            {loading
                                ? 'Processing...'
                                : (
                                    <>
                                        {mode === 'buy' ? 'Confirm Purchase' : 'Confirm Sale'}
                                        <DollarSign className="w-5 h-5 fill-white/20" />
                                    </>
                                )
                            }
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )
}
