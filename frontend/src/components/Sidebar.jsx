import { useState, useEffect } from 'react'
import { NavLink } from 'react-router-dom'
import { fetchTransactionHistory, fetchPendingTransactions } from '../services/api'
import {
    LayoutDashboard,
    Package,
    BarChart3,
    Truck,
    Bell,
    Settings,
    LogOut,
    Menu
} from 'lucide-react'

const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Home' },
    { path: '/inventory', icon: Package, label: 'Inventory' },
    // { path: '/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/suppliers', icon: Truck, label: 'Suppliers' },
    { path: '/alerts', icon: Bell, label: 'Alerts', badge: 3 },
]

function Sidebar({ isOpen, onClose }) {
    const [transactions, setTransactions] = useState([])
    const [pending, setPending] = useState([])

    useEffect(() => {
        const loadTransactions = async () => {
            try {
                const [historyData, pendingData] = await Promise.all([
                    fetchTransactionHistory(10),
                    fetchPendingTransactions(5)
                ])
                setTransactions(historyData)
                setPending(pendingData)
            } catch (error) {
                console.error("Failed to load transactions", error)
            }
        }

        loadTransactions()
        // Poll every 5 seconds to keep queue visualization live
        const interval = setInterval(loadTransactions, 2000)
        return () => clearInterval(interval)
    }, [])

    return (
        <aside className={`sidebar-new ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'} group flex flex-col`}>
            {/* Logo Area */}
            <div className="h-[64px] shrink-0 flex items-center justify-center border-b border-slate-200">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-orange-500 to-violet-600 flex items-center justify-center shadow-lg shadow-violet-200">
                    <span className="text-white font-bold text-xl">S</span>
                </div>
                <div className="hidden group-hover:block ml-3 overflow-hidden whitespace-nowrap transition-all duration-300">
                    <h1 className="text-lg font-bold text-slate-800 tracking-wide">StockFlow</h1>
                </div>
            </div>

            {/* Navigation */}
            <nav className="mt-6 px-2 space-y-2 shrink-0">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        onClick={onClose}
                        className={({ isActive }) =>
                            `flex items-center px-4 py-3 rounded-xl transition-all duration-200 group/link relative ${isActive
                                ? 'bg-gradient-to-r from-violet-100 to-orange-50 text-violet-700'
                                : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'
                            }`
                        }
                    >
                        {({ isActive }) => (
                            <>
                                <div className={`absolute left-0 w-1 h-8 rounded-r-full bg-violet-500 transition-opacity ${isActive ? 'opacity-100' : 'opacity-0'}`} />
                                <item.icon className={`min-w-[24px] w-6 h-6 ${isActive ? 'text-violet-600' : 'text-slate-400 group-hover/link:text-slate-700'}`} />
                                <span className="hidden group-hover:block ml-4 font-medium whitespace-nowrap animate-fade-in">
                                    {item.label}
                                </span>
                                {item.badge && (
                                    <span className="hidden group-hover:flex absolute right-4 w-5 h-5 bg-red-500 text-white text-[10px] items-center justify-center rounded-full font-bold">
                                        {item.badge}
                                    </span>
                                )}
                            </>
                        )}
                    </NavLink>
                ))}
            </nav>

            {/* Transaction Queue Visualization */}
            <div className="mt-auto px-4 pb-20 flex flex-col overflow-hidden">
                <div className="mb-2 flex items-center justify-between">
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Transaction Queue</h3>
                    <span className="text-[10px] bg-violet-100 text-violet-600 px-2 py-0.5 rounded-full font-bold">FIFO</span>
                </div>

                <div className="flex-1 overflow-y-auto space-y-2 pr-1 max-h-[200px] scrollbar-thin">
                    {/* Pending Items (Front of Queue) */}
                    {pending.map((tx) => (
                        <div key={tx.id} className="bg-orange-50 border border-orange-100 rounded-lg p-2.5 flex items-center gap-3 animate-pulse">
                            <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center shrink-0">
                                <span className="text-orange-600 text-xs font-bold">Q</span>
                            </div>
                            <div className="overflow-hidden">
                                <p className="text-xs font-bold text-slate-700 truncate">{tx.product_id}</p>
                                <p className="text-[10px] text-orange-600 font-medium">{tx.type} • {tx.quantity} units</p>
                            </div>
                        </div>
                    ))}

                    {/* History Items */}
                    {transactions.map((tx) => (
                        <div key={tx.id} className="bg-white border border-slate-100 rounded-lg p-2.5 flex items-center gap-3 hover:border-violet-200 transition-colors">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${tx.type === 'sale' ? 'bg-emerald-100 text-emerald-600' : 'bg-blue-100 text-blue-600'
                                }`}>
                                {tx.type === 'sale' ? '$' : 'R'}
                            </div>
                            <div className="overflow-hidden">
                                <p className="text-xs font-bold text-slate-700 truncate">{tx.product_id}</p>
                                <p className="text-[10px] text-slate-400 font-medium capitalize">
                                    {tx.type} • {tx.quantity} units
                                </p>
                            </div>
                        </div>
                    ))}

                    {transactions.length === 0 && pending.length === 0 && (
                        <div className="text-center py-4 text-slate-400 text-xs">
                            Queue Empty
                        </div>
                    )}
                </div>
            </div>

            {/* Bottom Profile Section */}
            <div className="absolute bottom-6 left-0 right-0 px-2 lg:px-4 bg-white/80 backdrop-blur-sm pt-2">
                <div className="flex items-center p-2 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer hover:border-violet-300 transition-colors">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold text-sm shrink-0">
                        R
                    </div>
                    <div className="hidden group-hover:block ml-3 overflow-hidden">
                        <p className="text-sm font-medium text-slate-800 truncate">Rishab</p>
                        <p className="text-[10px] text-slate-500 truncate">Dept of AIML</p>
                    </div>
                </div>
            </div>
        </aside>
    )
}

export default Sidebar

