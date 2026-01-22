# Stock Monitoring & Inventory Management System
## 🎓 Final Year DSA + Data Science Project

A comprehensive inventory management system that demonstrates **6+ core data structures** combined with **data science analytics** and a modern **React frontend**.

![Dashboard Preview](https://via.placeholder.com/800x400?text=StockFlow+Dashboard)

## 🚀 Features

### Data Structures Implemented
| Data Structure | Use Case | Time Complexity |
|----------------|----------|-----------------|
| **HashMap** | O(1) product lookup by ID | O(1) avg |
| **AVL Tree** | Price/quantity range queries | O(log n) |
| **Min-Heap** | Low stock priority alerts | O(log n) |
| **Max-Heap** | Top sellers ranking | O(log n) |
| **Trie** | Product name autocomplete | O(m) |
| **Graph** | Supplier network, shortest path | O(V+E) |
| **Queue** | FIFO transaction processing | O(1) |

### Data Science Features
- 📈 **Demand Forecasting** - SMA, EMA, Linear Regression
- 📊 **Trend Analysis** - Seasonality detection, growth rates
- 🔍 **Anomaly Detection** - Z-score based outliers
- 📉 **Visualizations** - Matplotlib charts, Recharts

### Modern React Frontend
- 🎨 Glassmorphism UI design
- 📱 Fully responsive
- 📊 Interactive Recharts dashboards
- 🔄 Real-time WebSocket updates

## 📁 Project Structure

```
Stock-Monitoring-and-Inventory-Management/
├── backend/
│   ├── core/
│   │   ├── data_structures/    # Custom DSA implementations
│   │   │   ├── hashmap.py      # HashMap with chaining
│   │   │   ├── avl_tree.py     # Self-balancing BST
│   │   │   ├── heap.py         # Min/Max Heap
│   │   │   ├── trie.py         # Prefix tree
│   │   │   ├── graph.py        # Weighted graph
│   │   │   └── queue.py        # Transaction queue
│   │   ├── inventory_engine.py # Main DSA engine
│   │   └── models.py           # Data models
│   ├── analytics/
│   │   ├── forecasting.py      # Demand prediction
│   │   ├── trend_analyzer.py   # Trend analysis
│   │   └── visualizations.py   # Chart generation
│   ├── api/
│   │   └── main.py             # FastAPI backend
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
└── README.md
```

## 🛠️ Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend/api
python main.py
# Server runs on http://localhost:8000
```

### Start Frontend Development Server
```bash
cd frontend
npm run dev
# UI runs on http://localhost:3000
```

## 📚 DSA Concepts Demonstrated

### 1. HashMap (O(1) Operations)
```python
# Custom implementation with chaining
class HashMap:
    def put(self, key, value):  # O(1) average
    def get(self, key):         # O(1) average
    def remove(self, key):      # O(1) average
```

### 2. AVL Tree (Range Queries)
```python
# Self-balancing BST
class AVLTree:
    def insert(self, key, value):      # O(log n)
    def range_query(self, low, high):  # O(log n + k)
```

### 3. Binary Heap (Priority Alerts)
```python
# Min-Heap for low stock alerts
class MinHeap:
    def push(self, item):   # O(log n)
    def pop(self):          # O(log n)
```

### 4. Trie (Autocomplete)
```python
# Prefix tree for search
class Trie:
    def insert(self, key):           # O(m)
    def autocomplete(self, prefix):  # O(m + k)
```

### 5. Graph (Supplier Network)
```python
# Weighted directed graph
class Graph:
    def dijkstra(self, start):  # O((V+E) log V)
    def bfs(self, start):       # O(V + E)
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products` | GET | List all products |
| `/api/products/{id}` | GET | Get product by ID |
| `/api/products` | POST | Create product |
| `/api/transactions` | POST | Queue transaction |
| `/api/analytics/forecast` | POST | Get demand forecast |
| `/api/alerts/low-stock` | GET | Get low stock alerts |
| `/api/suppliers/network` | GET | Get supplier graph |

## 🎯 Academic Value

This project demonstrates:
- ✅ Custom implementation of 6+ data structures
- ✅ Time complexity analysis for all operations
- ✅ Real-world application of DSA concepts
- ✅ Integration with Data Science (NumPy, Matplotlib)
- ✅ Full-stack development (FastAPI + React)
- ✅ Modern software engineering practices

## 👥 Team

- **Project**: Stock Monitoring & Inventory Management
- **Course**: Data Structures & Algorithms
- **Type**: Final Year Experiential Learning Project

## 📄 License

This project is for educational purposes.
