# 
# FastAPI Backend for Stock Monitoring System
# ============================================
# REST API and WebSocket endpoints for the inventory management system.
# 

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
    # Request model for creating a product.# 
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
    # Request model for updating a product.# 
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
    # Request model for creating a transaction.# 
    product_id: str
    transaction_type: str = Field(..., pattern="^(sale|restock|return|adjustment)$")
    quantity: int = Field(..., gt=0)
    unit_price: Optional[float] = None


class SupplierCreate(BaseModel):
    # Request model for creating a supplier.# 
    id: str
    name: str
    contact_email: str = ""
    contact_phone: str = ""
    address: str = ""
    lead_time_days: int = 7
    products: List[str] = []


class ForecastRequest(BaseModel):
    # Request model for forecast.# 
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
    # Application lifespan - initialize and cleanup.# 
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
    # Load sample data for demonstration.# 
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
    # API root endpoint.# 
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
#     
#     Get all products with optional filtering.
#     
#     DSA Used:
#     
#     if search:
#         # Use Trie for search - O(m + k)
#         products = engine.search_products(search, limit)
#     elif min_price is not None and max_price is not None:
#         # Use AVL Tree for range query - O(log n + k)
#         products = engine.get_products_in_price_range(min_price, max_price)
#     else:
#         # Get all products - O(n)
#         products = engine.get_all_products()
#     
#     # Apply additional filters
#     if category and category.lower() != 'all':
#         products = [p for p in products if p.category.lower() == category.lower()]
#     
#     if low_stock_only:
#         products = [p for p in products if p.is_low_stock]
#     
#     return {
#         "count": len(products),
#         "products": [p.to_dict() for p in products[:limit]]
#     }
# 
# 
# @app.get("/api/products/{product_id}", tags=["Products"])
# async def get_product(product_id: str):
#     
    Get a single product by ID.
    
    DSA Used: HashMap - O(1)
#     
#     product = engine.get_product(product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
#     return product.to_dict()
# 
# 
# @app.post("/api/products", tags=["Products"])
# async def create_product(product_data: ProductCreate):
#     
    Create a new product.
    
    DSA Used:
    - HashMap for storage
    - AVL Tree for indexing
    - Trie for search
    - Heap for alerts
#     
#     product = Product(
#         id=product_data.id,
#         name=product_data.name,
#         category=product_data.category,
#         sku=product_data.sku or product_data.id,
#         quantity=product_data.quantity,
#         price=product_data.price,
#         cost=product_data.cost,
#         threshold=product_data.threshold,
#         reorder_point=product_data.reorder_point,
#         reorder_quantity=product_data.reorder_quantity,
#         supplier_id=product_data.supplier_id,
#         description=product_data.description,
#         tags=product_data.tags
#     )
#     
#     success, message = engine.add_product(product)
#     
#     if not success:
#         raise HTTPException(status_code=400, detail=message)
#     
#     # Broadcast update
#     await manager.broadcast({
#         "type": "product_added",
#         "product": product.to_dict()
#     })
#     
#     return {"success": True, "message": message, "product": product.to_dict()}
# 
# 
# @app.put("/api/products/{product_id}", tags=["Products"])
# async def update_product(product_id: str, updates: ProductUpdate):
    # Update a product.# 
#     update_dict = {k: v for k, v in updates.dict().items() if v is not None}
#     
#     if not update_dict:
#         raise HTTPException(status_code=400, detail="No updates provided")
#     
#     success, message = engine.update_product(product_id, update_dict)
#     
#     if not success:
#         raise HTTPException(status_code=404, detail=message)
#     
#     product = engine.get_product(product_id)
#     
#     # Broadcast update
#     await manager.broadcast({
#         "type": "product_updated",
#         "product": product.to_dict()
#     })
#     
#     return {"success": True, "message": message, "product": product.to_dict()}
# 
# 
# @app.delete("/api/products/{product_id}", tags=["Products"])
# async def delete_product(product_id: str):
    # Delete a product.# 
#     success, message = engine.delete_product(product_id)
#     
#     if not success:
#         raise HTTPException(status_code=404, detail=message)
#     
#     await manager.broadcast({
#         "type": "product_deleted",
#         "product_id": product_id
#     })
#     
#     return {"success": True, "message": message}
# 
# 
# @app.get("/api/products/search/{query}", tags=["Products"])
# async def search_products(query: str, limit: int = 10):
#     
    Search products by name prefix.
    
    DSA Used: Trie autocomplete - O(m + k)
#     
#     products = engine.search_products(query, limit)
#     return {
#         "query": query,
#         "count": len(products),
#         "results": [p.to_dict() for p in products]
#     }
# 
# 
# # =====================================
# # API Routes - Transactions
# # =====================================
# 
# @app.post("/api/transactions", tags=["Transactions"])
# async def create_transaction(transaction: TransactionCreate):
#     
    Queue a new transaction.
    
    DSA Used: Queue enqueue - O(1)
#     
#     tx = engine.queue_transaction(
#         product_id=transaction.product_id,
#         trans_type=transaction.transaction_type,
#         quantity=transaction.quantity,
#         unit_price=transaction.unit_price or 0
#     )
#     
#     return {
#         "success": True,
#         "message": "Transaction queued",
#         "transaction": tx.to_dict()
#     }
# 
# 
# @app.post("/api/transactions/process", tags=["Transactions"])
# async def process_transactions(batch_size: int = 10):
#     
    Process pending transactions.
    
    DSA Used:
    - Queue dequeue - O(1)
    - HashMap update - O(1)
    - AVL Tree update - O(log n)
    - Heap update - O(log n)
#     
#     results = engine.process_pending_transactions(batch_size)
#     
#     if results:
#         await manager.broadcast({
#             "type": "transactions_processed",
#             "count": len(results)
#         })
#     
#     return {
#         "processed": len(results),
#         "results": results
#     }
# 
# 
# @app.get("/api/transactions/pending", tags=["Transactions"])
# async def get_pending_transactions(limit: int = 20):
    # Get pending transactions.# 
#     pending = engine.transaction_queue.peek_pending(limit)
#     return {
#         "count": len(pending),
#         "transactions": [tx.to_dict() for tx in pending]
#     }
# 
# 
# @app.get("/api/transactions/history", tags=["Transactions"])
# async def get_transaction_history(limit: int = 50):
    # Get transaction history.# 
#     history = engine.transaction_queue.get_history(limit)
#     return {
#         "count": len(history),
#         "transactions": [tx.to_dict() for tx in history]
#     }
# 
# 
# # =====================================
# # API Routes - Alerts
# # =====================================
# 
# @app.get("/api/alerts/low-stock", tags=["Alerts"])
# async def get_low_stock_alerts(limit: int = 10):
#     
    Get low stock alerts.
    
    DSA Used: Min-Heap - O(k log n)
#     
#     alerts = engine.get_low_stock_alerts(limit)
#     return {
#         "count": len(alerts),
#         "alerts": [p.to_dict() for p in alerts]
#     }
# 
# 
# @app.get("/api/alerts/top-sellers", tags=["Alerts"])
# async def get_top_sellers(limit: int = 10):
#     
    Get top selling products.
    
    DSA Used: Max-Heap - O(k log n)
#     
#     sellers = engine.get_top_sellers(limit)
#     return {
#         "count": len(sellers),
#         "products": [p.to_dict() for p in sellers]
#     }
# 
# 
# # =====================================
# # API Routes - Analytics
# # =====================================
# 
# @app.get("/api/analytics/summary", tags=["Analytics"])
# async def get_inventory_summary():
    # Get inventory summary statistics.# 
#     summary = engine.get_summary()
#     return summary.to_dict()
# 
# 
# @app.post("/api/analytics/forecast", tags=["Analytics"])
# async def get_forecast(request: ForecastRequest):
#     
    Get demand forecast for a product.
    
    Uses time series analysis with SMA, EMA, or linear regression.
#     
#     product = engine.get_product(request.product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     
#     # Generate sample historical data for demo
#     # In production, this would come from transaction history
#     import random
#     import numpy as np
#     
#     base_demand = product.velocity if product.velocity > 0 else 10
#     historical = [max(0, base_demand + random.gauss(0, base_demand * 0.3)) 
#                   for _ in range(60)]
#     
#     forecaster = DemandForecaster()
#     forecast = forecaster.forecast(
#         product_id=request.product_id,
#         historical_data=historical,
#         periods=request.periods,
#         method=request.method
#     )
#     
#     return forecast.to_dict()
# 
# 
# @app.get("/api/analytics/health", tags=["Analytics"])
# async def get_inventory_health():
    # Get inventory health score.# 
#     products = [p.to_dict() for p in engine.get_all_products()]
#     health = analytics.get_inventory_health_score(products)
#     return health
# 
# 
# @app.get("/api/analytics/trends/{product_id}", tags=["Analytics"])
# async def get_product_trends(product_id: str):
    # Get trend analysis for a product.# 
#     product = engine.get_product(product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     
#     # Generate sample data for demo
#     import random
#     sales_data = [max(0, 10 + random.gauss(0, 3)) for _ in range(30)]
#     dates = [(datetime.now().replace(day=1)).strftime('%Y-%m-%d') 
#              for _ in range(30)]
#     
#     trend_analyzer = TrendAnalyzer()
#     trend = trend_analyzer.analyze(product_id, sales_data, dates)
#     
#     return trend.to_dict()
# 
# 
# # =====================================
# # API Routes - Suppliers
# # =====================================
# 
# @app.get("/api/suppliers", tags=["Suppliers"])
# async def get_all_suppliers():
    # Get all suppliers.# 
#     suppliers = list(engine.suppliers.values())
#     return {
#         "count": len(suppliers),
#         "suppliers": [s.to_dict() for s in suppliers]
#     }
# 
# 
# @app.post("/api/suppliers", tags=["Suppliers"])
# async def create_supplier(supplier_data: SupplierCreate):
#     
    Add a new supplier.
    
    DSA Used: Graph vertex/edge addition
#     
#     supplier = Supplier(
#         id=supplier_data.id,
#         name=supplier_data.name,
#         contact_email=supplier_data.contact_email,
#         contact_phone=supplier_data.contact_phone,
#         address=supplier_data.address,
#         lead_time_days=supplier_data.lead_time_days,
#         products=supplier_data.products
#     )
#     
#     success, message = engine.add_supplier(supplier)
#     
#     if not success:
#         raise HTTPException(status_code=400, detail=message)
#     
#     return {"success": True, "message": message, "supplier": supplier.to_dict()}
# 
# 
# @app.get("/api/suppliers/network", tags=["Suppliers"])
# async def get_supplier_network():
#     
    Get supplier network analysis.
    
    DSA Used: Graph algorithms (centrality, components)
#     
#     analysis = engine.get_supplier_network_analysis()
#     graph_data = engine.supplier_graph.to_dict()
#     
#     return {
#         "analysis": analysis,
#         "graph": graph_data
#     }
# 
# 
# @app.get("/api/suppliers/for-product/{product_id}", tags=["Suppliers"])
# async def get_suppliers_for_product(product_id: str):
#     
    Find suppliers for a product.
    
    DSA Used: Graph traversal - O(V + E)
#     
#     suppliers = engine.get_suppliers_for_product(product_id)
#     fastest = engine.find_fastest_supplier(product_id)
#     
#     return {
#         "product_id": product_id,
#         "suppliers": [s.to_dict() for s in suppliers],
#         "fastest_supplier": {
#             "supplier": fastest[0].to_dict() if fastest else None,
#             "lead_time_days": fastest[1] if fastest else None
#         }
#     }
# 
# 
# # =====================================
# # API Routes - Visualizations
# # =====================================
# 
# @app.get("/api/visualizations/inventory-levels", tags=["Visualizations"])
# async def get_inventory_levels_chart():
    # Generate inventory levels chart.# 
#     products = engine.get_all_products()
#     chart = visualizer.plot_inventory_levels(
#         [p.to_dict() for p in products[:15]],
#         title="Current Inventory Levels"
#     )
#     return {"chart": chart}
# 
# 
# @app.get("/api/visualizations/categories", tags=["Visualizations"])
# async def get_category_chart():
    # Generate category distribution chart.# 
#     summary = engine.get_summary()
#     chart = visualizer.plot_category_distribution(
#         summary.categories,
#         title="Products by Category"
#     )
#     return {"chart": chart}
# 
# 
# @app.get("/api/visualizations/top-sellers", tags=["Visualizations"])
# async def get_top_sellers_chart():
    # Generate top sellers chart.# 
#     sellers = engine.get_top_sellers(10)
#     chart = visualizer.plot_top_sellers(
#         [p.to_dict() for p in sellers],
#         title="Top Selling Products"
#     )
#     return {"chart": chart}
# 
# 
# @app.get("/api/visualizations/health-gauge", tags=["Visualizations"])
# async def get_health_gauge():
    # Generate health score gauge.# 
#     products = [p.to_dict() for p in engine.get_all_products()]
#     health = analytics.get_inventory_health_score(products)
#     chart = visualizer.plot_health_gauge(
#         health['score'],
#         health['grade'],
#         title="Inventory Health Score"
#     )
#     return {"chart": chart, "health": health}
# 
# 
# # =====================================
# # WebSocket
# # =====================================
# 
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     # WebSocket for real-time updates
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_json({"received": data})
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
# 
# 
# # =====================================
# # Run Server
# # =====================================
# 
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# 