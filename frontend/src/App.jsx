import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Inventory from './pages/Inventory'
import Analytics from './pages/Analytics'
import Suppliers from './pages/Suppliers'
import Alerts from './pages/Alerts'

function App() {
    const [sidebarOpen, setSidebarOpen] = useState(false)

    return (
        <Router>
            <div className="min-h-screen">
                {/* Sidebar */}
                <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

                {/* Main Content */}
                <div className="lg:ml-64 min-h-screen">
                    {/* Mobile Header */}
                    <div className="lg:hidden fixed top-0 left-0 right-0 z-40 glass px-4 py-3">
                        <button
                            onClick={() => setSidebarOpen(true)}
                            className="p-2 rounded-lg hover:bg-gray-100"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                    </div>

                    {/* Page Content */}
                    <main className="p-4 lg:p-8 pt-16 lg:pt-8">
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/inventory" element={<Inventory />} />
                            <Route path="/analytics" element={<Analytics />} />
                            <Route path="/suppliers" element={<Suppliers />} />
                            <Route path="/alerts" element={<Alerts />} />
                        </Routes>
                    </main>
                </div>

                {/* Mobile Overlay */}
                {sidebarOpen && (
                    <div
                        className="lg:hidden fixed inset-0 bg-black/50 z-40"
                        onClick={() => setSidebarOpen(false)}
                    />
                )}
            </div>
        </Router>
    )
}

export default App
