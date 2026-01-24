
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import InventoryEngine

def test_load():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    state_file = os.path.join(data_dir, 'inventory_state.json')
    
    print(f"Testing load from: {state_file}")
    
    engine = InventoryEngine(data_dir=data_dir)
    success, message = engine.load_from_json(state_file)
    
    if success:
        print("SUCCESS: Data loaded.")
        print(message)
        # Verify days_of_stock
        products = engine.get_all_products()
        for p in products:
            print(f"Product {p.id}: days_of_stock={p.days_of_stock}")
    else:
        print("FAILURE: Could not load data.")
        print(message)

if __name__ == "__main__":
    test_load()
