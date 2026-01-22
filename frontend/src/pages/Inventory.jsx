import { useState, useEffect } from 'react'
import {
    Search,
    Plus,
    Filter,
    MoreVertical,
    Edit,
    Trash2,
    Package,
    ArrowUpDown,
    Download,
    Upload
} from 'lucide-react'

// Sample product data
const sampleProducts = [
    { id: 'PROD001', name: 'Wireless Mouse', category: 'Electronics', sku: 'WM-001', quantity: 150, price: 999, cost: 450, threshold: 20, total_sold: 1250, is_low_stock: false },
    { id: 'PROD002', name: 'USB Keyboard', category: 'Electronics', sku: 'UK-002', quantity: 85, price: 1499, cost: 700, threshold: 15, total_sold: 890, is_low_stock: false },
    { id: 'PROD003', name: 'Monitor Stand', category: 'Furniture', sku: 'MS-003', quantity: 45, price: 2499, cost: 1200, threshold: 10, total_sold: 650, is_low_stock: false },
    { id: 'PROD004', name: 'Webcam HD', category: 'Electronics', sku: 'WC-004', quantity: 12, price: 3999, cost: 1800, threshold: 15, total_sold: 520, is_low_stock: true },
    { id: 'PROD005', name: 'Desk Lamp', category: 'Furniture', sku: 'DL-005', quantity: 200, price: 799, cost: 350, threshold: 25, total_sold: 430, is_low_stock: false },
    { id: 'PROD006', name: 'Headphones', category: 'Electronics', sku: 'HP-006', quantity: 8, price: 2999, cost: 1400, threshold: 20, total_sold: 480, is_low_stock: true },
    { id: 'PROD007', name: 'Mouse Pad XL', category: 'Electronics', sku: 'MP-007', quantity: 300, price: 499, cost: 150, threshold: 30, total_sold: 920, is_low_stock: false },
    { id: 'PROD008', name: 'USB Hub', category: 'Electronics', sku: 'UH-008', quantity: 0, price: 1299, cost: 600, threshold: 15, total_sold: 340, is_low_stock: true },
    { id: 'PROD009', name: 'Cable Organizer', category: 'Home', sku: 'CO-009', quantity: 180, price: 299, cost: 100, threshold: 20, total_sold: 670, is_low_stock: false },
    { id: 'PROD010', name: 'Laptop Stand', category: 'Furniture', sku: 'LS-010', quantity: 55, price: 1999, cost: 900, threshold: 10, total_sold: 380, is_low_stock: false },
]

function Inventory() {
    const [products, setProducts] = useState(sampleProducts)
    const [searchQuery, setSearchQuery] = useState('')
    const [selectedCategory, setSelectedCategory] = useState('all')
    const [showAddModal, setShowAddModal] = useState(false)
    const [sortConfig, setSortConfig] = useState({ key: 'name', direction: 'asc' })

    const categories = ['all', 'Electronics', 'Furniture', 'Home', 'Food', 'Other']

    // Filter and sort products
    const filteredProducts = products
        .filter(p => {
            const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                p.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                p.sku.toLowerCase().includes(searchQuery.toLowerCase())
            const matchesCategory = selectedCategory === 'all' || p.category === selectedCategory
            return matchesSearch && matchesCategory
        })
        .sort((a, b) => {
            if (a[sortConfig.key] < b[sortConfig.key]) return sortConfig.direction === 'asc' ? -1 : 1
            if (a[sortConfig.key] > b[sortConfig.key]) return sortConfig.direction === 'asc' ? 1 : -1
            return 0
        })

    const handleSort = (key) => {
        setSortConfig(prev => ({
            key,
            direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
        }))
    }

    const getStockStatus = (product) => {
        if (product.quantity === 0) return { label: 'Out of Stock', class: 'badge-danger' }
        if (product.is_low_stock) return { label: 'Low Stock', class: 'badge-warning' }
        return { label: 'In Stock', class: 'badge-success' }
    }

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="flex flex-col lg:flex-row lg:items-center justify-between mb-6 gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Inventory Management</h1>
                    <p className="text-gray-500">
                        <span className="text-primary-600 font-medium">HashMap O(1)</span> lookup •
                        <span className="text-primary-600 font-medium"> Trie</span> autocomplete search
                    </p>
                </div>
                <div className="flex items-center gap-3">
                    <button className="btn-secondary">
                        <Download className="w-4 h-4" />
                        Export
                    </button>
                    <button className="btn-secondary">
                        <Upload className="w-4 h-4" />
                        Import
                    </button>
                    <button className="btn-primary" onClick={() => setShowAddModal(true)}>
                        <Plus className="w-4 h-4" />
                        Add Product
                    </button>
                </div>
            </div>

            {/* Filters Row */}
            <div className="card p-4 mb-6">
                <div className="flex flex-col lg:flex-row gap-4">
                    {/* Search */}
                    <div className="flex-1 input-group">
                        <Search className="input-icon w-5 h-5" />
                        <input
                            type="text"
                            placeholder="Search products by name, ID, or SKU... (Trie O(m) lookup)"
                            className="input-with-icon"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    {/* Category Filter */}
                    <div className="flex items-center gap-2">
                        <Filter className="w-5 h-5 text-gray-400" />
                        <select
                            className="input w-48"
                            value={selectedCategory}
                            onChange={(e) => setSelectedCategory(e.target.value)}
                        >
                            {categories.map(cat => (
                                <option key={cat} value={cat}>
                                    {cat === 'all' ? 'All Categories' : cat}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>

            {/* Products Table */}
            <div className="table-container overflow-x-auto">
                <table className="w-full min-w-[800px]">
                    <thead>
                        <tr>
                            <th className="table-header">
                                <button onClick={() => handleSort('id')} className="flex items-center gap-1 hover:text-gray-700">
                                    ID <ArrowUpDown className="w-3 h-3" />
                                </button>
                            </th>
                            <th className="table-header">
                                <button onClick={() => handleSort('name')} className="flex items-center gap-1 hover:text-gray-700">
                                    Product <ArrowUpDown className="w-3 h-3" />
                                </button>
                            </th>
                            <th className="table-header">Category</th>
                            <th className="table-header">
                                <button onClick={() => handleSort('quantity')} className="flex items-center gap-1 hover:text-gray-700">
                                    Quantity <ArrowUpDown className="w-3 h-3" />
                                </button>
                            </th>
                            <th className="table-header">
                                <button onClick={() => handleSort('price')} className="flex items-center gap-1 hover:text-gray-700">
                                    Price <ArrowUpDown className="w-3 h-3" />
                                </button>
                            </th>
                            <th className="table-header">Status</th>
                            <th className="table-header">
                                <button onClick={() => handleSort('total_sold')} className="flex items-center gap-1 hover:text-gray-700">
                                    Sold <ArrowUpDown className="w-3 h-3" />
                                </button>
                            </th>
                            <th className="table-header text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredProducts.map((product) => {
                            const status = getStockStatus(product)
                            return (
                                <tr key={product.id} className="table-row">
                                    <td className="table-cell font-mono text-sm text-primary-600">{product.id}</td>
                                    <td className="table-cell">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-100 to-purple-100 flex items-center justify-center">
                                                <Package className="w-5 h-5 text-primary-600" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900">{product.name}</p>
                                                <p className="text-xs text-gray-500">SKU: {product.sku}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="table-cell">
                                        <span className="badge-info">{product.category}</span>
                                    </td>
                                    <td className="table-cell">
                                        <div className="flex items-center gap-2">
                                            <span className={`font-semibold ${product.quantity === 0 ? 'text-danger-600' :
                                                    product.is_low_stock ? 'text-warning-600' : 'text-gray-900'
                                                }`}>
                                                {product.quantity}
                                            </span>
                                            <span className="text-xs text-gray-400">/ {product.threshold}</span>
                                        </div>
                                    </td>
                                    <td className="table-cell font-semibold">₹{product.price.toLocaleString()}</td>
                                    <td className="table-cell">
                                        <span className={status.class}>{status.label}</span>
                                    </td>
                                    <td className="table-cell text-gray-600">{product.total_sold.toLocaleString()}</td>
                                    <td className="table-cell text-right">
                                        <div className="flex items-center justify-end gap-2">
                                            <button className="p-2 hover:bg-gray-100 rounded-lg text-gray-500 hover:text-primary-600">
                                                <Edit className="w-4 h-4" />
                                            </button>
                                            <button className="p-2 hover:bg-gray-100 rounded-lg text-gray-500 hover:text-danger-600">
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

            {/* Summary Footer */}
            <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
                <p>Showing {filteredProducts.length} of {products.length} products</p>
                <p className="text-primary-600">
                    🔍 Search uses <strong>Trie</strong> for O(m) prefix matching •
                    Data stored in <strong>HashMap</strong> for O(1) access
                </p>
            </div>

            {/* Add Product Modal */}
            {showAddModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
                    <div className="card w-full max-w-lg p-6 animate-slide-up">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-bold">Add New Product</h2>
                            <button onClick={() => setShowAddModal(false)} className="p-2 hover:bg-gray-100 rounded-lg">
                                ✕
                            </button>
                        </div>
                        <form className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Product ID</label>
                                    <input type="text" className="input" placeholder="PROD001" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">SKU</label>
                                    <input type="text" className="input" placeholder="WM-001" />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
                                <input type="text" className="input" placeholder="Wireless Mouse" />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                                    <select className="input">
                                        {categories.filter(c => c !== 'all').map(cat => (
                                            <option key={cat} value={cat}>{cat}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                                    <input type="number" className="input" placeholder="100" />
                                </div>
                            </div>
                            <div className="grid grid-cols-3 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Price (₹)</label>
                                    <input type="number" className="input" placeholder="999" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Cost (₹)</label>
                                    <input type="number" className="input" placeholder="450" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Threshold</label>
                                    <input type="number" className="input" placeholder="20" />
                                </div>
                            </div>
                            <div className="flex justify-end gap-3 pt-4">
                                <button type="button" className="btn-secondary" onClick={() => setShowAddModal(false)}>
                                    Cancel
                                </button>
                                <button type="submit" className="btn-primary">
                                    <Plus className="w-4 h-4" />
                                    Add Product
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Inventory
