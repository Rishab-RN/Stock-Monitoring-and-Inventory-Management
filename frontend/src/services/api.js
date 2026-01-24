import axios from 'axios'

const API_URL = 'http://localhost:8080/api'

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

export const fetchProducts = async (params = {}) => {
    try {
        const response = await api.get('/products', { params })
        return response.data
    } catch (error) {
        console.error('Error fetching products:', error)
        throw error
    }
}

export const fetchSummary = async () => {
    try {
        const response = await api.get('/analytics/summary')
        return response.data
    } catch (error) {
        console.error('Error fetching summary:', error)
        throw error
    }
}

export const fetchTopSellers = async () => { // Uses Max-Heap
    try {
        const response = await api.get('/alerts/top-sellers')
        return response.data.products
    } catch (error) {
        console.error('Error fetching top sellers:', error)
        throw error
    }
}

export const fetchLowStock = async () => { // Uses Min-Heap
    try {
        const response = await api.get('/alerts/low-stock')
        return response.data.alerts
    } catch (error) {
        console.error('Error fetching low stock:', error)
        throw error
    }
}

export const searchProducts = async (query) => { // Uses Trie
    try {
        const response = await api.get(`/products/search/${query}`)
        return response.data.results
    } catch (error) {
        console.error('Error searching products:', error)
        throw error
    }
}


export const createProduct = async (productData) => {
    try {
        const response = await api.post('/products', productData)
        return response.data
    } catch (error) {
        console.error('Error creating product:', error)
        throw error
    }
}

export const deleteProduct = async (productId) => {
    try {
        const response = await api.delete(`/products/${productId}`)
        return response.data
    } catch (error) {
        console.error('Error deleting product:', error)
        throw error
    }
}

export const createSupplier = async (supplierData) => {
    try {
        const response = await api.post('/suppliers', supplierData)
        return response.data
    } catch (error) {
        console.error('Error creating supplier:', error)
        throw error
    }
}

export const createTransaction = async (transactionData) => {
    try {
        const response = await api.post('/transactions', transactionData)
        return response.data
    } catch (error) {
        console.error('Error creating transaction:', error)
        throw error
    }
}

export const processTransactions = async () => {
    try {
        const response = await api.post('/transactions/process')
        return response.data
    } catch (error) {
        console.error('Error processing transactions:', error)
        throw error
    }
}

export const fetchTransactionHistory = async (limit = 50) => {
    try {
        const response = await api.get('/transactions/history', { params: { limit } })
        return response.data.transactions
    } catch (error) {
        console.error('Error fetching transaction history:', error)
        throw error
    }
}

export const fetchPendingTransactions = async (limit = 20) => {
    try {
        const response = await api.get('/transactions/pending', { params: { limit } })
        return response.data.transactions
    } catch (error) {
        console.error('Error fetching pending transactions:', error)
        throw error
    }
}

export default api
