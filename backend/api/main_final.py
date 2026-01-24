# docstring removed

import os
import sys
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import InventoryEngine, Product, Supplier, AlertSeverity
from analytics import DemandForecaster, TrendAnalyzer, InventoryAnalytics, InventoryVisualizer


# =====================================
# Pydantic Models for Request/Response
# =====================================

class ProductCreate(BaseModel):
    # docstring removed
    id: str = Field(..., description="Unique product ID")
    name: str = Field(..., description="Product name")
    category: str = Field(default="Other", description="Product category")
    sku: str = Field(default="", description="Stock keeping unit")
    quantity: int = Field(default=0, ge=0, description="Current quantity")
    price: float = Field(..., gt=0, description="Selling price")
    cost: float = Field(default=0, ge=0, description="Cost price")
    threshold: int = Field(default=10, ge=0, description="Low stock threshold")
    reorder_point: int = Field(default=20, ge=0, description="Reorder trigger point")
    reorder_quantity: int = Field(default=50, ge=0, description="Default reorder amount")
    supplier_id: Optional[str] = None
    description: str = ""
    tags: List[str] = []


class ProductUpdate(BaseModel):
    # docstring removed
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    threshold: Optional[int] = None
    reorder_point: Optional[int] = None
    reorder_quantity: Optional[int] = None
    supplier_id: Optional[str] = None
    description: Optional[str] = None


class TransactionCreate(BaseModel):
    # docstring removed
    product_id: str
    transaction_type: str = Field(..., pattern="^(sale|restock|return|adjustment)$")
    quantity: int = Field(..., gt=0)
    unit_price: Optional[float] = None


class SupplierCreate(BaseModel):
    # docstring removed
    id: str
    name: str
    contact_email: str = ""
    contact_phone: str = ""
    address: str = ""
    lead_time_days: int = 7
    products: List[str] = []


class ForecastRequest(BaseModel):
    # docstring removed
    product_id: str
    periods: int = Field(default=30, ge=1, le=90)
    method: str = Field(default="auto", pattern="^(auto|sma|ema|linear)$")


# =====================================
# Application Setup
# =====================================

# Global engine instance
engine: Optional[InventoryEngine] = None
analytics: Optional[InventoryAnalytics] = None
visualizer: Optional[InventoryVisualizer] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # docstring removed
    global engine, analytics, visualizer
    
    # Initialize
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    engine = InventoryEngine(data_dir=data_dir)
    analytics = InventoryAnalytics()
    visualizer = InventoryVisualizer()
    
    # Try to load existing data
    state_file = os.path.join(data_dir, 'inventory_state.json')
    if os.path.exists(state_file):
        engine.load_from_json(state_file)
    else:
        # Load sample data for demo
        _load_sample_data()
    
    print("✅ Inventory Engine initialized")
    
    yield
    
    # Cleanup - save state
    os.makedirs(data_dir, exist_ok=True)
    engine.save_to_json(state_file)
    print("✅ State saved")


def _load_sample_data():
    # docstring removed
    sample_products = [
        {"id": "PROD001", "name": "Wireless Mouse", "category": "Electronics", "quantity": 150, "price": 999, "cost": 450, "threshold": 20},
        {"id": "PROD002", "name": "USB Keyboard", "category": "Electronics", "quantity": 85, "price": 1499, "cost": 700, "threshold": 15},
        {"id": "PROD003", "name": "Monitor Stand", "category": "Furniture", "quantity": 45, "price": 2499, "cost": 1200, "threshold": 10},
        {"id": "PROD004", "name": "Webcam HD", "category": "Electronics", "quantity": 12, "price": 3999, "cost": 1800, "threshold": 15},
        {"id": "PROD005", "name": "Desk Lamp", "category": "Furniture", "quantity": 200, "price": 799, "cost": 350, "threshold": 25},
        {"id": "PROD006", "name": "Headphones", "category": "Electronics", "quantity": 8, "price": 2999, "cost": 1400, "threshold": 20},
        {"id": "PROD007", "name": "Mouse Pad XL", "category": "Electronics", "quantity": 300, "price": 499, "cost": 150, "threshold": 30},
        {"id": "PROD008", "name": "USB Hub", "category": "Electronics", "quantity": 0, "price": 1299, "cost": 600, "threshold": 15},
        {"id": "PROD009", "name": "Cable Organizer", "category": "Home", "quantity": 180, "price": 299, "cost": 100, "threshold": 20},
        {"id": "PROD010", "name": "Laptop Stand", "category": "Furniture", "quantity": 55, "price": 1999, "cost": 900, "threshold": 10},
    ]
    
    for p_data in sample_products:
        product = Product(
            id=p_data["id"],
            name=p_data["name"],
            category=p_data["category"],
            sku=p_data["id"],
            quantity=p_data["quantity"],
            price=p_data["price"],
            cost=p_data["cost"],
            threshold=p_data["threshold"],
            reorder_point=p_data["threshold"] * 2,
            reorder_quantity=p_data["threshold"] * 5
        )
        engine.add_product(product)


# Create FastAPI app
app = FastAPI(
    title="Stock Monitoring & Inventory Management API",
    description="DSA-powered inventory management with analytics and forecasting",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================
# API Routes - Products
# =====================================

@app.get("/")
async def root():
    # docstring removed
    return {
        "name": "Stock Monitoring & Inventory Management API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "products": "/api/products",
            "transactions": "/api/transactions",
            "analytics": "/api/analytics",
            "suppliers": "/api/suppliers",
            "websocket": "/ws"
        }
    }


@app.get("/api/products", tags=["Products"])
async def get_all_products(
    category: Optional[str] = None,
    low_stock_only: bool = False,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = Query(default=100, le=500)
):
    # docstring removed
    Get a single product by ID.
    
    DSA Used: HashMap - O(1)
    # docstring removed
    Create a new product.
    
    DSA Used:
    - HashMap for storage
    - AVL Tree for indexing
    - Trie for search
    - Heap for alerts
    # docstring removedUpdate a product.# docstring removedDelete a product.# docstring removed
    Search products by name prefix.
    
    DSA Used: Trie autocomplete - O(m + k)
    # docstring removed
    Queue a new transaction.
    
    DSA Used: Queue enqueue - O(1)
    # docstring removed
    Process pending transactions.
    
    DSA Used:
    - Queue dequeue - O(1)
    - HashMap update - O(1)
    - AVL Tree update - O(log n)
    - Heap update - O(log n)
    # docstring removedGet pending transactions.# docstring removedGet transaction history.# docstring removed
    Get low stock alerts.
    
    DSA Used: Min-Heap - O(k log n)
    # docstring removed
    Get top selling products.
    
    DSA Used: Max-Heap - O(k log n)
    # docstring removedGet inventory summary statistics.# docstring removed
    Get demand forecast for a product.
    
    Uses time series analysis with SMA, EMA, or linear regression.
    # docstring removedGet inventory health score.# docstring removedGet trend analysis for a product.# docstring removedGet all suppliers.# docstring removed
    Add a new supplier.
    
    DSA Used: Graph vertex/edge addition
    # docstring removed
    Get supplier network analysis.
    
    DSA Used: Graph algorithms (centrality, components)
    # docstring removed
    Find suppliers for a product.
    
    DSA Used: Graph traversal - O(V + E)
    # docstring removedGenerate inventory levels chart.# docstring removedGenerate category distribution chart.# docstring removedGenerate top sellers chart.# docstring removedGenerate health score gauge."""
    products = [p.to_dict() for p in engine.get_all_products()]
    health = analytics.get_inventory_health_score(products)
    chart = visualizer.plot_health_gauge(
        health['score'],
        health['grade'],
        title="Inventory Health Score"
    )
    return {"chart": chart, "health": health}


# =====================================
# WebSocket
# =====================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # WebSocket for real-time updates
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"received": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# =====================================
# Run Server
# =====================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

