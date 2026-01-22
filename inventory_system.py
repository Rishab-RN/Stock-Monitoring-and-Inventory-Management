from collections import deque
import heapq
from datetime import datetime

class Product:
def init(self, pid, name, category, qty, price, threshold):
    self.id = pid
    self.name = name
    self.category = category
    self.quantity = qty
    self.price = price
    self.threshold = threshold
    self.total_sold = 0
    self.history = [] # later can be treated like BST/time-based

class InventorySystem:
    def init(self):
    # Hash Map: product_id -> Product
    self.products = {}
    # Queue: transactions
    self.transaction_queue = deque()
    # Heaps
    self.top_sellers_heap = [] # max-heap via negative values
    self.low_stock_heap = [] # min-heap
    # Stats
    self.total_transactions = 0
    self.total_units_sold = 0

# ---------- HASH MAP ----------
def add_product(self, pid, name, category, qty, price, threshold):
    if pid in self.products:
        return False, "Product ID already exists"
    p = Product(pid, name, category, qty, price, threshold)
    self.products[pid] = p
    if qty < threshold:
        heapq.heappush(self.low_stock_heap, (qty, pid))
    return True, f"Product {name} added successfully"

def get_product(self, pid):
    return self.products.get(pid)

def update_quantity(self, pid, new_qty):
    if pid not in self.products:
        return False, "Product not found"
    p = self.products[pid]
    p.quantity = new_qty
    if new_qty < p.threshold:
        heapq.heappush(self.low_stock_heap, (new_qty, pid))
    return True, "Quantity updated"

def display_all_products(self):
    if not self.products:
        return "No products in inventory"
    lines = []
    lines.append("="*80)
    lines.append(f"{'ID':<8} {'Name':<20} {'Category':<15} {'Qty':<8} {'Price':<10} {'Sold':<8}")
    lines.append("="*80)
    for pid, p in self.products.items():
        lines.append(f"{pid:<8} {p.name:<20} {p.category:<15} {p.quantity:<8} ₹{p.price:<9} {p.total_sold:<8}")
    lines.append("="*80)
    return "\n".join(lines)

# ---------- QUEUE ----------
def enqueue_transaction(self, pid, ttype, qty, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    self.transaction_queue.append({
        "product_id": pid,
        "type": ttype,
        "quantity": qty,
        "timestamp": timestamp
    })
    return True

def process_transactions(self):
    results = []
    while self.transaction_queue:
        tran = self.transaction_queue.popleft()
        msg = self._process_single_transaction(tran)
        results.append(msg)
        self.total_transactions += 1
    return results

def _process_single_transaction(self, tran):
    pid = tran["product_id"]
    ttype = tran["type"]
    qty = tran["quantity"]
    ts = tran["timestamp"]

    if pid not in self.products:
        return f"Error: product {pid} not found"

    p = self.products[pid]

    if ttype == "sale":
        if p.quantity < qty:
            return f"Error: insufficient stock for {pid}"
        p.quantity -= qty
        p.total_sold += qty
        self.total_units_sold += qty
        heapq.heappush(self.top_sellers_heap, (-p.total_sold, pid))
        if p.quantity < p.threshold:
            heapq.heappush(self.low_stock_heap, (p.quantity, pid))
        msg = f"✓ Sale: {qty} units of {p.name}"
    elif ttype == "restock":
        p.quantity += qty
        msg = f"✓ Restock: {qty} units of {p.name}"
    elif ttype == "return":
        p.quantity += qty
        msg = f"✓ Return: {qty} units of {p.name}"
    else:
        msg = f"Error: unknown transaction type {ttype}"

    p.history.append((ts, qty, ttype))
    return msg

# ---------- HEAPS ----------
def get_top_sellers(self, n=5):
    if not self.top_sellers_heap:
        return "No sales data available"
    temp = self.top_sellers_heap.copy()
    result = []
    seen = set()
    while temp and len(result) < n:
        sold_neg, pid = heapq.heappop(temp)
        if pid in self.products and pid not in seen:
            p = self.products[pid]
            result.append((p.name, p.total_sold))
            seen.add(pid)
    return result

def get_low_stock_alerts(self):
    alerts = []
    temp = self.low_stock_heap.copy()
    seen = set()
    while temp:
        qty, pid = heapq.heappop(temp)
        if pid in self.products and pid not in seen:
            p = self.products[pid]
            if p.quantity < p.threshold:
                alerts.append({
                    "id": pid,
                    "name": p.name,
                    "current_qty": p.quantity,
                    "threshold": p.threshold,
                    "shortage": p.threshold - p.quantity
                })
                seen.add(pid)
    return alerts

# ---------- SUMMARY ----------
def get_inventory_summary(self):
    total_products = len(self.products)
    total_value = sum(p.quantity * p.price for p in self.products.values())
    low_stock_count = len(self.get_low_stock_alerts())
    return (
        f"Inventory Summary:\n"
        f"Total Products: {total_products}\n"
        f"Total Inventory Value: ₹{total_value:,.2f}\n"
        f"Total Transactions: {self.total_transactions}\n"
        f"Total Units Sold: {self.total_units_sold}\n"
        f"Low Stock Alerts: {low_stock_count}\n"
    )
