import { NavLink } from 'react-router-dom'
import {
    LayoutDashboard,
    Package,
    BarChart3,
    Truck,
    Bell,
    Settings,
    LogOut,
    X
} from 'lucide-react'

const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard', description: 'Overview & KPIs' },
    { path: '/inventory', icon: Package, label: 'Inventory', description: 'Product Management' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics', description: 'Trends & Forecasts' },
    { path: '/suppliers', icon: Truck, label: 'Suppliers', description: 'Supply Network' },
    { path: '/alerts', icon: Bell, label: 'Alerts', description: 'Notifications', badge: 3 },
]

function Sidebar({ isOpen, onClose }) {
    return (
        <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
            {/* Logo */}
            <div className="flex items-center justify-between px-6 py-6">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
                        <Package className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-white">StockFlow</h1>
                        <p className="text-xs text-gray-400">DSA Powered</p>
                    </div>
                </div>
                <button
                    onClick={onClose}
                    className="lg:hidden p-2 text-gray-400 hover:text-white rounded-lg hover:bg-white/10"
                >
                    <X className="w-5 h-5" />
                </button>
            </div>

            {/* Navigation */}
            <nav className="mt-6 space-y-1">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        onClick={onClose}
                        className={({ isActive }) =>
                            `sidebar-link ${isActive ? 'active' : ''}`
                        }
                    >
                        <item.icon className="w-5 h-5" />
                        <div className="flex-1">
                            <span className="font-medium">{item.label}</span>
                            <p className="text-xs opacity-60">{item.description}</p>
                        </div>
                        {item.badge && (
                            <span className="px-2 py-0.5 text-xs font-medium bg-red-500 text-white rounded-full">
                                {item.badge}
                            </span>
                        )}
                    </NavLink>
                ))}
            </nav>

            {/* DSA Info */}
            <div className="absolute bottom-24 left-4 right-4">
                <div className="p-4 rounded-xl bg-gradient-to-br from-primary-500/20 to-purple-500/20 border border-white/10">
                    <h3 className="text-sm font-semibold text-white mb-2">📚 DSA Concepts</h3>
                    <ul className="text-xs text-gray-300 space-y-1">
                        <li>• HashMap - O(1) Lookup</li>
                        <li>• AVL Tree - Range Queries</li>
                        <li>• Heap - Priority Alerts</li>
                        <li>• Trie - Autocomplete</li>
                        <li>• Graph - Supplier Network</li>
                    </ul>
                </div>
            </div>

            {/* Footer */}
            <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/10">
                <div className="flex items-center gap-3 px-2">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary-400 to-purple-400 flex items-center justify-center text-white text-sm font-medium">
                        A
                    </div>
                    <div className="flex-1">
                        <p className="text-sm font-medium text-white">Admin</p>
                        <p className="text-xs text-gray-400">Final Year Project</p>
                    </div>
                    <button className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-white/10">
                        <Settings className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </aside>
    )
}

export default Sidebar
