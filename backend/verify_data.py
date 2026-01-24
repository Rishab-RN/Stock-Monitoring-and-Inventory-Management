
import json
import os
import sys

# Add parent to path to import models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from core import InventoryEngine

try:
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    print(f"Loading data from {data_dir}")
    
    engine = InventoryEngine(data_dir=data_dir)
    state_file = os.path.join(data_dir, 'inventory_state.json')
    
    success, msg = engine.load_from_json(state_file)
    print(f"Load result: {success}, {msg}")
    
    if success:
        print(f"Engine has {len(engine.products)} products")
        print("Getting all products...")
        prods = engine.get_all_products()
        print(f"Retrieved {len(prods)} products")
        if len(prods) > 0:
            print(f"Sample: {prods[0].to_dict()}")
            
except Exception as e:
    print(f"Fatal verification error: {e}")
    import traceback
    traceback.print_exc()
