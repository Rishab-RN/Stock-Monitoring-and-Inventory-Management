"""
Inventory Engine - Core DSA Integration
========================================
Main engine that integrates all data structures for
efficient inventory management operations.

DSA Concepts Used:
- HashMap: O(1) product lookup
- AVL Tree: O(log n) range queries
- Min-Heap: O(log n) low stock alerts
- Max-Heap: O(log n) top sellers
- Trie: O(m) autocomplete search
- Graph: O(V+E) supplier network
- Queue: O(1) transaction processing
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import uuid

# Import custom data structures
from .data_structures.hashmap import HashMap
from .data_structures.avl_tree import AVLTree
from .data_structures.heap import MinHeap, MaxHeap, PriorityQueue
from .data_structures.trie import Trie
from .data_structures.graph import Graph
from .data_structures.queue import TransactionQueue, Transaction

from .models import Product, Supplier, Alert, AlertSeverity, InventorySummary


class InventoryEngine:
    """
    Main inventory management engine using custom data structures.
    
    This class demonstrates practical applications of various DSA concepts
    in a real-world inventory management system.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the inventory engine with all data structures.
        
        Args:
            data_dir: Directory for persisting data (optional)
        """
        self.data_dir = data_dir
        
        # ===============================
        # HASHMAP: O(1) Product Lookup
        # ===============================
        # Primary storage for products - enables constant-time access by ID
        self.products = HashMap()
        
        # ===============================
        # AVL TREE: O(log n) Range Queries
        # ===============================
        # For efficient price/quantity range queries
        self.price_tree = AVLTree()
        self.quantity_tree = AVLTree()
        
        # ===============================
        # HEAP: O(log n) Priority Operations
        # ===============================
        # Min-Heap for low stock alerts (lowest stock = highest priority)
        self.low_stock_heap = MinHeap(key_func=lambda x: x[0])  # (quantity, product_id)
        # Max-Heap for top sellers (highest sales = top)
        self.top_sellers_heap = MaxHeap(key_func=lambda x: x[0])  # (sales, product_id)
        # Priority Queue for alerts
        self.alert_queue = PriorityQueue()
        
        # ===============================
        # TRIE: O(m) Prefix Search
        # ===============================
        # For product name autocomplete
        self.product_trie = Trie(case_sensitive=False)
        
        # ===============================
        # GRAPH: Supplier Network
        # ===============================
        # Supplier-product relationships
        self.supplier_graph = Graph(directed=True)
        
        # ===============================
        # QUEUE: FIFO Transaction Processing
        # ===============================
        self.transaction_queue = TransactionQueue()
        
        # Supplier storage (using HashMap)
        self.suppliers = HashMap()
        
        # Statistics
        self.stats = {
            'total_transactions': 0,
            'total_sales': 0,
            'total_revenue': 0.0,
            'created_at': datetime.now().isoformat()
        }
        
        # Alert counter
        self._alert_counter = 0
    
    # ====================
    # PRODUCT OPERATIONS
    # ====================
    
    def add_product(self, product: Product) -> Tuple[bool, str]:
        """
        Add a new product to inventory.
        
        Time Complexity: O(m) where m is product name length
        (dominated by Trie insertion)
        
        DSA Used:
        - HashMap: O(1) for storage
        - AVL Tree: O(log n) for indexing
        - Trie: O(m) for searchability
        """
        if product.id in self.products:
            return False, f"Product {product.id} already exists"
        
        # Store in HashMap - O(1)
        self.products[product.id] = product
        
        # Index in AVL Trees - O(log n)
        self.price_tree.insert(product.price, product.id)
        self.quantity_tree.insert(product.quantity, product.id)
        
        # Add to Trie for search - O(m)
        self.product_trie.insert(product.name, product.id)
        
        # Check for low stock alert
        if product.is_low_stock:
            self._create_low_stock_alert(product)
            
        # Add to Min-Heap (Low Stock) - O(log n)
        self.low_stock_heap.push((product.quantity, product.id))
        
        # Add to Max-Heap (Top Sellers) - O(log n)
        if product.total_sold > 0:
            self.top_sellers_heap.push((product.total_sold, product.id))
        
        return True, f"Product '{product.name}' added successfully"
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """
        Get product by ID.
        
        Time Complexity: O(1) - HashMap lookup
        """
        return self.products.get(product_id)
    
    def update_product(self, product_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Update product attributes.
        
        Time Complexity: O(log n) due to AVL tree updates
        """
        product = self.products.get(product_id)
        if not product:
            return False, f"Product {product_id} not found"
        
        old_price = product.price
        old_quantity = product.quantity
        old_name = product.name
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        product.updated_at = datetime.now()
        
        # Update AVL trees if price/quantity changed - O(log n)
        if product.price != old_price:
            self.price_tree.delete(old_price)
            self.price_tree.insert(product.price, product_id)
        
        if product.quantity != old_quantity:
            self.quantity_tree.delete(old_quantity)
            self.quantity_tree.insert(product.quantity, product_id)
            self._update_stock_heap(product)
        
        # Update Trie if name changed - O(m)
        if product.name != old_name:
            self.product_trie.delete(old_name)
            self.product_trie.insert(product.name, product_id)
        
        return True, f"Product '{product.name}' updated"
    
    def delete_product(self, product_id: str) -> Tuple[bool, str]:
        """
        Remove a product from inventory.
        
        Time Complexity: O(log n + m)
        """
        product = self.products.get(product_id)
        if not product:
            return False, f"Product {product_id} not found"
        
        # Remove from all data structures
        self.products.remove(product_id)
        self.price_tree.delete(product.price)
        self.quantity_tree.delete(product.quantity)
        self.product_trie.delete(product.name)
        
        return True, f"Product '{product.name}' deleted"
    
    def search_products(self, query: str, limit: int = 10) -> List[Product]:
        """
        Search products by name prefix.
        
        Time Complexity: O(m + k) where m is query length, k is results
        
        DSA Used: Trie autocomplete
        """
        results = self.product_trie.autocomplete(query, limit)
        products = []
        for name, product_id in results:
            product = self.products.get(product_id)
            if product:
                products.append(product)
        return products
    
    def get_products_in_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """
        Get products within a price range.
        
        Time Complexity: O(log n + k) where k is number of results
        
        DSA Used: AVL Tree range query
        """
        results = self.price_tree.range_query(min_price, max_price)
        products = []
        for price, product_id in results:
            product = self.products.get(product_id)
            if product:
                products.append(product)
        return products
    
    def get_products_by_quantity_range(self, min_qty: int, max_qty: int) -> List[Product]:
        """
        Get products within a quantity range.
        
        Time Complexity: O(log n + k)
        
        DSA Used: AVL Tree range query
        """
        results = self.quantity_tree.range_query(min_qty, max_qty)
        products = []
        for qty, product_id in results:
            product = self.products.get(product_id)
            if product:
                products.append(product)
        return products
    
    # ====================
    # TRANSACTION PROCESSING
    # ====================
    
    def queue_transaction(self, product_id: str, trans_type: str, 
                          quantity: int, unit_price: float = 0) -> Transaction:
        """
        Queue a transaction for processing.
        
        Time Complexity: O(1)
        
        DSA Used: Queue (FIFO)
        """
        product = self.products.get(product_id)
        if product and unit_price == 0:
            unit_price = product.price
        
        return self.transaction_queue.enqueue(
            product_id=product_id,
            transaction_type=trans_type,
            quantity=quantity,
            unit_price=unit_price
        )
    
    def process_pending_transactions(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """
        Process queued transactions.
        
        Time Complexity: O(batch_size * log n)
        
        DSA Used: Queue dequeue, Heap updates
        """
        results = []
        
        for _ in range(batch_size):
            transaction = self.transaction_queue.dequeue()
            if not transaction:
                break
            
            result = self._process_transaction(transaction)
            self.transaction_queue.complete(transaction, result['success'])
            results.append(result)
        
        return results
    
    def _process_transaction(self, transaction: Transaction) -> Dict[str, Any]:
        """Process a single transaction."""
        product = self.products.get(transaction.product_id)
        if not product:
            return {'success': False, 'error': 'Product not found', 'transaction': transaction.to_dict()}
        
        try:
            if transaction.transaction_type == 'sale':
                return self._process_sale(product, transaction)
            elif transaction.transaction_type == 'restock':
                return self._process_restock(product, transaction)
            elif transaction.transaction_type == 'return':
                return self._process_return(product, transaction)
            elif transaction.transaction_type == 'adjustment':
                return self._process_adjustment(product, transaction)
            else:
                return {'success': False, 'error': f'Unknown transaction type: {transaction.transaction_type}'}
        except Exception as e:
            return {'success': False, 'error': str(e), 'transaction': transaction.to_dict()}
    
    def _process_sale(self, product: Product, transaction: Transaction) -> Dict[str, Any]:
        """Process a sale transaction."""
        if product.quantity < transaction.quantity:
            return {
                'success': False,
                'error': f'Insufficient stock. Available: {product.quantity}, Requested: {transaction.quantity}'
            }
        
        # Update quantity
        old_qty = product.quantity
        product.quantity -= transaction.quantity
        product.total_sold += transaction.quantity
        product.total_revenue += transaction.total_value
        product.updated_at = datetime.now()
        
        # Update AVL tree - O(log n)
        self.quantity_tree.delete(old_qty)
        self.quantity_tree.insert(product.quantity, product.id)
        
        # Update heaps
        self._update_stock_heap(product)
        self._update_sales_heap(product)
        
        # Update stats
        self.stats['total_transactions'] += 1
        self.stats['total_sales'] += transaction.quantity
        self.stats['total_revenue'] += transaction.total_value
        
        # Check for low stock
        if product.is_low_stock:
            self._create_low_stock_alert(product)
        
        return {
            'success': True,
            'message': f"Sold {transaction.quantity} units of {product.name}",
            'new_quantity': product.quantity,
            'transaction': transaction.to_dict()
        }
    
    def _process_restock(self, product: Product, transaction: Transaction) -> Dict[str, Any]:
        """Process a restock transaction."""
        old_qty = product.quantity
        product.quantity += transaction.quantity
        product.updated_at = datetime.now()
        
        # Update AVL tree
        self.quantity_tree.delete(old_qty)
        self.quantity_tree.insert(product.quantity, product.id)
        
        self._update_stock_heap(product)
        self.stats['total_transactions'] += 1
        
        return {
            'success': True,
            'message': f"Restocked {transaction.quantity} units of {product.name}",
            'new_quantity': product.quantity,
            'transaction': transaction.to_dict()
        }
    
    def _process_return(self, product: Product, transaction: Transaction) -> Dict[str, Any]:
        """Process a return transaction."""
        old_qty = product.quantity
        product.quantity += transaction.quantity
        product.updated_at = datetime.now()
        
        self.quantity_tree.delete(old_qty)
        self.quantity_tree.insert(product.quantity, product.id)
        
        self._update_stock_heap(product)
        self.stats['total_transactions'] += 1
        
        return {
            'success': True,
            'message': f"Returned {transaction.quantity} units of {product.name}",
            'new_quantity': product.quantity,
            'transaction': transaction.to_dict()
        }
    
    def _process_adjustment(self, product: Product, transaction: Transaction) -> Dict[str, Any]:
        """Process an inventory adjustment."""
        old_qty = product.quantity
        product.quantity = transaction.quantity  # Set to exact value
        product.updated_at = datetime.now()
        
        self.quantity_tree.delete(old_qty)
        self.quantity_tree.insert(product.quantity, product.id)
        
        self._update_stock_heap(product)
        self.stats['total_transactions'] += 1
        
        return {
            'success': True,
            'message': f"Adjusted {product.name} quantity from {old_qty} to {product.quantity}",
            'new_quantity': product.quantity,
            'transaction': transaction.to_dict()
        }
    
    # ====================
    # ALERTS & PRIORITY
    # ====================
    
    def _update_stock_heap(self, product: Product) -> None:
        """Update low stock heap after quantity change."""
        self.low_stock_heap.push((product.quantity, product.id))
    
    def _update_sales_heap(self, product: Product) -> None:
        """Update top sellers heap after sale."""
        self.top_sellers_heap.push((product.total_sold, product.id))
    
    def _create_low_stock_alert(self, product: Product) -> Alert:
        """Create a low stock alert."""
        self._alert_counter += 1
        
        # Determine severity
        ratio = product.quantity / product.threshold if product.threshold > 0 else 0
        if product.quantity == 0:
            severity = AlertSeverity.CRITICAL
            alert_type = 'out_of_stock'
        elif ratio < 0.25:
            severity = AlertSeverity.HIGH
            alert_type = 'low_stock'
        elif ratio < 0.5:
            severity = AlertSeverity.MEDIUM
            alert_type = 'low_stock'
        else:
            severity = AlertSeverity.LOW
            alert_type = 'low_stock'
        
        alert = Alert(
            id=f"ALERT-{self._alert_counter:06d}",
            product_id=product.id,
            alert_type=alert_type,
            severity=severity,
            message=f"{product.name}: Stock at {product.quantity} units (threshold: {product.threshold})",
            quantity=product.quantity,
            threshold=product.threshold
        )
        
        # Add to priority queue
        self.alert_queue.push(alert, alert.priority_score)
        
        return alert
    
    def get_low_stock_alerts(self, limit: int = 10) -> List[Product]:
        """
        Get products with lowest stock levels.
        
        Time Complexity: O(k log n) where k is limit
        
        DSA Used: Min-Heap
        """
        alerts = []
        seen = set()
        
        # Use a copy to not consume the heap
        temp_items = []
        
        while len(alerts) < limit and self.low_stock_heap:
            item = self.low_stock_heap.pop()
            if item:
                qty, product_id = item
                temp_items.append(item)
                
                if product_id not in seen:
                    product = self.products.get(product_id)
                    if product and product.is_low_stock:
                        alerts.append(product)
                        seen.add(product_id)
        
        # Restore items
        for item in temp_items:
            self.low_stock_heap.push(item)
        
        return alerts
    
    def get_top_sellers(self, limit: int = 10) -> List[Product]:
        """
        Get top selling products.
        
        Time Complexity: O(k log n) where k is limit
        
        DSA Used: Max-Heap
        """
        sellers = []
        seen = set()
        temp_items = []
        
        while len(sellers) < limit and self.top_sellers_heap:
            item = self.top_sellers_heap.pop()
            if item:
                sales, product_id = item
                temp_items.append(item)
                
                if product_id not in seen:
                    product = self.products.get(product_id)
                    if product and product.total_sold > 0:
                        sellers.append(product)
                        seen.add(product_id)
        
        # Restore items
        for item in temp_items:
            self.top_sellers_heap.push(item)
        
        return sellers
    
    def get_priority_alerts(self, limit: int = 10) -> List[Alert]:
        """
        Get highest priority alerts.
        
        DSA Used: Priority Queue
        """
        alerts = []
        for _ in range(limit):
            result = self.alert_queue.peek()
            if result:
                alert, priority = result
                alerts.append(alert)
                self.alert_queue.pop()
        return alerts
    
    # ====================
    # SUPPLIER NETWORK
    # ====================
    
    def add_supplier(self, supplier: Supplier) -> Tuple[bool, str]:
        """
        Add a supplier to the network.
        
        Time Complexity: O(p) where p is number of products
        """
        if supplier.id in self.suppliers:
            return False, f"Supplier {supplier.id} already exists"
        
        self.suppliers[supplier.id] = supplier
        
        # Add to graph
        self.supplier_graph.add_vertex(f"SUP_{supplier.id}", supplier.to_dict())
        
        # Link to products
        for product_id in supplier.products:
            if product_id in self.products:
                self.supplier_graph.add_vertex(f"PROD_{product_id}")
                # Edge from supplier to product with lead time as weight
                self.supplier_graph.add_edge(
                    f"SUP_{supplier.id}",
                    f"PROD_{product_id}",
                    weight=supplier.lead_time_days
                )
        
        return True, f"Supplier '{supplier.name}' added"
    
    def get_suppliers_for_product(self, product_id: str) -> List[Supplier]:
        """
        Find all suppliers for a product.
        
        Time Complexity: O(V + E)
        
        DSA Used: Graph traversal
        """
        suppliers = []
        product_node = f"PROD_{product_id}"
        
        # Find all vertices connected to this product
        for v in self.supplier_graph.vertices:
            if v.startswith("SUP_"):
                neighbors = self.supplier_graph.get_neighbors(v)
                for neighbor, weight in neighbors:
                    if neighbor == product_node:
                        supplier_id = v.replace("SUP_", "")
                        supplier = self.suppliers.get(supplier_id)
                        if supplier:
                            suppliers.append(supplier)
        
        return suppliers
    
    def find_fastest_supplier(self, product_id: str) -> Optional[Tuple[Supplier, int]]:
        """
        Find supplier with shortest lead time for a product.
        
        Time Complexity: O(V + E)
        
        DSA Used: Graph edge weights
        """
        suppliers = self.get_suppliers_for_product(product_id)
        if not suppliers:
            return None
        
        best = min(suppliers, key=lambda s: s.lead_time_days)
        return (best, best.lead_time_days)
    
    def get_supplier_network_analysis(self) -> Dict[str, Any]:
        """
        Analyze the supplier network.
        
        DSA Used: Graph centrality metrics
        """
        centrality = self.supplier_graph.degree_centrality()
        components = self.supplier_graph.get_connected_components()
        
        return {
            'total_nodes': len(self.supplier_graph),
            'total_edges': self.supplier_graph.edge_count,
            'connected_components': len(components),
            'centrality_scores': {
                k: round(v, 3) for k, v in 
                sorted(centrality.items(), key=lambda x: -x[1])[:10]
            }
        }
    
    # ====================
    # SUMMARY & ANALYTICS
    # ====================
    
    def get_summary(self) -> InventorySummary:
        """
        Get complete inventory summary.
        
        Time Complexity: O(n)
        """
        products = list(self.products.values())
        
        total_quantity = sum(p.quantity for p in products)
        total_value = sum(p.stock_value for p in products)
        low_stock = sum(1 for p in products if p.is_low_stock)
        out_of_stock = sum(1 for p in products if p.quantity == 0)
        
        # Category breakdown
        categories = {}
        for p in products:
            categories[p.category] = categories.get(p.category, 0) + 1
        
        # Top sellers
        top_selling = [
            {'id': p.id, 'name': p.name, 'sold': p.total_sold, 'revenue': p.total_revenue}
            for p in sorted(products, key=lambda x: -x.total_sold)[:5]
        ]
        
        return InventorySummary(
            total_products=len(products),
            total_quantity=total_quantity,
            total_value=total_value,
            low_stock_count=low_stock,
            out_of_stock_count=out_of_stock,
            pending_orders=self.transaction_queue.pending_count,
            total_sales=self.stats['total_sales'],
            total_revenue=self.stats['total_revenue'],
            categories=categories,
            top_selling=top_selling
        )
    
    def get_all_products(self) -> List[Product]:
        """Get all products as a list."""
        return list(self.products.values())
    
    # ====================
    # PERSISTENCE
    # ====================
    
    def save_to_json(self, filepath: str = None) -> str:
        """Save inventory state to JSON file."""
        if filepath is None:
            filepath = os.path.join(self.data_dir or '.', 'inventory_state.json')
        
        data = {
            'products': [p.to_dict() for p in self.products.values()],
            'suppliers': [s.to_dict() for s in self.suppliers.values()],
            'stats': self.stats,
            'saved_at': datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def load_from_json(self, filepath: str) -> Tuple[bool, str]:
        """Load inventory state from JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Clear existing data
            self.products = HashMap()
            self.suppliers = HashMap()
            self.price_tree = AVLTree()
            self.quantity_tree = AVLTree()
            self.product_trie = Trie(case_sensitive=False)
            
            # Load products
            for p_data in data.get('products', []):
                product = Product.from_dict(p_data)
                self.add_product(product)
            
            # Load suppliers
            for s_data in data.get('suppliers', []):
                supplier = Supplier.from_dict(s_data)
                self.add_supplier(supplier)
            
            self.stats = data.get('stats', self.stats)
            
            return True, f"Loaded {len(self.products)} products, {len(self.suppliers)} suppliers"
        
        except FileNotFoundError:
            return False, f"File not found: {filepath}"
        except Exception as e:
            return False, f"Error loading data: {str(e)}"
