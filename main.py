"""
Stock Monitoring & Inventory Optimization
Console Interface
"""

import csv
from datetime import datetime
from inventory_system import InventorySystem

def load_products_from_csv(system, filename):
    """Load initial products from CSV file"""
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                system.add_product(
                    row['product_id'],
                    row['name'],
                    row['category'],
                    int(row['initial_qty']),
                    float(row['price']),
                    int(row['threshold'])
                )
                count += 1
            return True, f"Loaded {count} products"
    except FileNotFoundError:
        return False, "Products file not found"
    except Exception as e:
        return False, f"Error: {str(e)}"


def load_transactions_from_csv(system, filename):
    """Load and queue transactions from CSV file"""
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                system.enqueue_transaction(
                    row['product_id'],
                    row['type'],
                    int(row['quantity']),
                    timestamp
                )
                count += 1
            return True, f"Queued {count} transactions"
    except FileNotFoundError:
        return False, "Transactions file not found"
    except Exception as e:
        return False, f"Error: {str(e)}"


def display_menu():
    """Display main menu"""
    menu = """
╔══════════════════════════════════════════════════════════╗
║     STOCK MONITORING & INVENTORY OPTIMIZATION            ║
║                 DSA Project Menu                         ║
╚══════════════════════════════════════════════════════════╝

1.  View All Products 
2.  Search Product 
3.  Add New Product 
4.  Update Stock Quantity 
5.  Process Transactions 
6.  View Top Sellers 
7.  View Low Stock Alerts 
8.  Inventory Summary
9.  Exit

"""
    print(menu)


def main():
    """Main application loop"""
    system = InventorySystem()

    print("\n Initializing Stock Monitoring System...")

    # Load initial data
    success, msg = load_products_from_csv(system, 'products.csv')
    print(f"   {msg}")

    success, msg = load_transactions_from_csv(system, 'transactions.csv')
    print(f"   {msg}")

    print("\n System ready!\n")

    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            # View all products using Hash Map
            print("\nCurrent Inventory (Hash Map Display):")
            print(system.display_all_products())
            input("\nPress Enter to continue...")

        elif choice == '2':
            # Search product using Hash Map O(1) lookup
            pid = input("\nEnter Product ID: ").strip().upper()
            product = system.get_product(pid)
            if product:
                print(f"\n✓ Product Found:")
                print(f"  ID: {product.id}")
                print(f"  Name: {product.name}")
                print(f"  Category: {product.category}")
                print(f"  Quantity: {product.quantity}")
                print(f"  Price: ₹{product.price}")
                print(f"  Total Sold: {product.total_sold}")
            else:
                print(f"\n✗ Product {pid} not found")
            input("\nPress Enter to continue...")

        elif choice == '3':
            # Add new product to Hash Map
            print("\n➕ Add New Product:")
            pid = input("Product ID: ").strip().upper()
            name = input("Name: ").strip()
            category = input("Category: ").strip()
            qty = int(input("Initial Quantity: "))
            price = float(input("Price: "))
            threshold = int(input("Low Stock Threshold: "))

            success, msg = system.add_product(pid, name, category, qty, price, threshold)
            print(f"\n{msg}")
            input("\nPress Enter to continue...")

        elif choice == '4':
            # Update quantity using Hash Map
            pid = input("\nEnter Product ID: ").strip().upper()
            new_qty = int(input("Enter new quantity: "))
            success, msg = system.update_quantity(pid, new_qty)
            print(f"\n{msg}")
            input("\nPress Enter to continue...")

        elif choice == '5':
            # Process all queued transactions
            print("\n⚙️  Processing Transaction Queue...")
            results = system.process_transactions()
            print(f"\nProcessed {len(results)} transactions:\n")
            for result in results:
                print(f"  {result}")
            input("\nPress Enter to continue...")

        elif choice == '6':
            # Display top sellers using Heap
            print("\n Top 5 Best Sellers (Heap Operation):")
            print("="*50)
            top_sellers = system.get_top_sellers(5)
            if isinstance(top_sellers, str):
                print(top_sellers)
            else:
                for i, (name, sold) in enumerate(top_sellers, 1):
                    print(f"{i}. {name:<30} {sold} units sold")
            print("="*50)
            input("\nPress Enter to continue...")

        elif choice == '7':
            # Display low stock alerts using Heap
            print("\n  Low Stock Alerts (Heap Operation):")
            print("="*70)
            alerts = system.get_low_stock_alerts()
            if not alerts:
                print("No low stock alerts - All products adequately stocked!")
            else:
                print(f"{'ID':<8} {'Product':<25} {'Current':<10} {'Threshold':<12} {'Shortage'}")
                print("-"*70)
                for alert in alerts:
                    print(f"{alert['id']:<8} {alert['name']:<25} {alert['current_qty']:<10} "
                          f"{alert['threshold']:<12} {alert['shortage']}")
            print("="*70)
            input("\nPress Enter to continue...")

        elif choice == '8':
            # Display inventory summary
            print(system.get_inventory_summary())
            input("\nPress Enter to continue...")

        elif choice == '9':
            print("\n Thank you for using Stock Monitoring System!")
            print("   DSA Concepts Demonstrated:")
            print("   ✓ Hash Map for O(1) operations")
            print("   ✓ Queue for ordered processing")
            print("   ✓ Heap for efficient ranking\n")
            break

        else:
            print("\n Invalid choice. Please select 1-9.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
