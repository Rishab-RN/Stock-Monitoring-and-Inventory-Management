import sys
import os
import random
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import InventoryEngine, Product, Supplier

def seed_inventory():
    print("🌱 Seeding inventory with sample data...")
    
    # Initialize engine with data persistence
    # Correct path: backend/data (same as main.py)
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    engine = InventoryEngine(data_dir=data_dir)
    
    # Check if data already exists
    if os.path.exists(os.path.join(data_dir, "inventory_state.json")):
        success, msg = engine.load_from_json(os.path.join(data_dir, "inventory_state.json"))
        if success and len(engine.products) > 0:
            print(f"✅ Data already exists: {msg}")
            return
            
    # Create Suppliers
    suppliers = [
        Supplier("SUP001", "Tech Components Ltd", "contact@techcomp.com", "+91-9876543210", "Mumbai", 3, 0.95, ["P001", "P002", "P005"]),
        Supplier("SUP002", "Office Comforts", "sales@officecomforts.com", "+91-9876543211", "Delhi", 5, 0.88, ["P003", "P004"]),
        Supplier("SUP003", "Global Gadgets", "info@globalgadgets.com", "+91-9876543212", "Bangalore", 2, 0.92, ["P006", "P007", "P008"]),
        Supplier("SUP004", "Home Essentials", "support@homeessentials.com", "+91-9876543213", "Pune", 4, 0.90, ["P009", "P010"])
    ]
    
    for s in suppliers:
        engine.add_supplier(s)
        print(f"  + Added supplier: {s.name}")

    # Create Products
    products = [
        # Electronics
        Product("P001", "Gaming Laptop Pro", "Electronics", "LAP-001", 15, 85000, 60000, 5, 10, 20),
        Product("P002", "Wireless Earbuds", "Electronics", "AUD-002", 45, 2500, 1200, 10, 20, 50),
        Product("P005", "4K Monitor 27\"", "Electronics", "MON-005", 8, 22000, 15000, 5, 8, 15),
        Product("P006", "Mechanical Keyboard", "Electronics", "ACC-006", 120, 4500, 2500, 20, 30, 50),
        Product("P007", "Gaming Mouse", "Electronics", "ACC-007", 5, 1800, 900, 10, 20, 40), # Low stock
        
        # Furniture
        Product("P003", "Ergonomic Chair", "Furniture", "FUR-003", 0, 12000, 8000, 5, 10, 20), # Out of stock
        Product("P004", "Standing Desk", "Furniture", "FUR-004", 12, 25000, 18000, 3, 5, 10),
        
        # Home
        Product("P009", "Smart Coffee Maker", "Home", "APP-009", 18, 8500, 5000, 5, 10, 15),
        Product("P010", "Air Purifier", "Home", "APP-010", 3, 15000, 10000, 5, 8, 12), # Low stock
        
        # More Items
        Product("P011", "USB-C Hub", "Electronics", "ACC-011", 200, 1200, 500, 30, 50, 100),
        Product("P012", "Webcam 1080p", "Electronics", "ACC-012", 4, 3500, 2000, 5, 10, 20) # Low stock
    ]

    for p in products:
        p.description = f"High quality {p.name.lower()} for professional use."
        p.tags = [p.category.lower(), "premium", "new"]
        engine.add_product(p)
        print(f"  + Added product: {p.name} (Qty: {p.quantity})")
        
        # Simulate some sales
        if p.quantity > 0:
            sold = random.randint(1, 5)
            p.total_sold = sold * 10 # Make them look popular
            p.total_revenue = p.total_sold * p.price
            # Manually update heaps since we modified attributes directly
            engine._update_sales_heap(p)

    # Save data
    engine.save_to_json()
    print("✅ Seed data successfully saved to inventory_state.json")

if __name__ == "__main__":
    seed_inventory()
