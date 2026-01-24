"""
Data Models for Stock Monitoring System
========================================
Pydantic models for type-safe data handling.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class ProductCategory(str, Enum):
    """Product category enumeration."""
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FOOD = "Food & Beverages"
    FURNITURE = "Furniture"
    TOOLS = "Tools & Hardware"
    SPORTS = "Sports & Outdoors"
    BEAUTY = "Beauty & Personal Care"
    HOME = "Home & Garden"
    AUTOMOTIVE = "Automotive"
    OTHER = "Other"


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    SALE = "sale"
    RESTOCK = "restock"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Product:
    """Product model with all attributes."""
    id: str
    name: str
    category: str
    sku: str
    quantity: int
    price: float
    cost: float
    threshold: int  # Low stock threshold
    reorder_point: int
    reorder_quantity: int
    supplier_id: Optional[str] = None
    location: str = "Main Warehouse"
    description: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Analytics fields
    total_sold: int = 0
    total_revenue: float = 0.0
    velocity: float = 0.0  # Units sold per day
    
    @property
    def stock_value(self) -> float:
        """Total value of current stock."""
        return self.quantity * self.cost
    
    @property
    def profit_margin(self) -> float:
        """Profit margin percentage."""
        if self.price == 0:
            return 0.0
        return ((self.price - self.cost) / self.price) * 100
    
    @property
    def is_low_stock(self) -> bool:
        """Check if stock is below threshold."""
        return self.quantity < self.threshold
    
    @property
    def needs_reorder(self) -> bool:
        """Check if reorder is needed."""
        return self.quantity <= self.reorder_point
    
    @property
    def days_of_stock(self) -> Optional[float]:
        """Estimated days of stock remaining."""
        if self.velocity <= 0:
            return None
        return self.quantity / self.velocity
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'sku': self.sku,
            'quantity': self.quantity,
            'price': self.price,
            'cost': self.cost,
            'threshold': self.threshold,
            'reorder_point': self.reorder_point,
            'reorder_quantity': self.reorder_quantity,
            'supplier_id': self.supplier_id,
            'location': self.location,
            'description': self.description,
            'tags': self.tags,
            'total_sold': self.total_sold,
            'total_revenue': self.total_revenue,
            'velocity': self.velocity,
            'stock_value': self.stock_value,
            'profit_margin': self.profit_margin,
            'is_low_stock': self.is_low_stock,
            'days_of_stock': self.days_of_stock,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            category=data.get('category', 'Other'),
            sku=data.get('sku', data['id']),
            quantity=data.get('quantity', 0),
            price=data.get('price', 0.0),
            cost=data.get('cost', 0.0),
            threshold=data.get('threshold', 10),
            reorder_point=data.get('reorder_point', 20),
            reorder_quantity=data.get('reorder_quantity', 50),
            supplier_id=data.get('supplier_id'),
            location=data.get('location', 'Main Warehouse'),
            description=data.get('description', ''),
            tags=data.get('tags', []),
            total_sold=data.get('total_sold', 0),
            total_revenue=data.get('total_revenue', 0.0),
            velocity=data.get('velocity', 0.0)
        )


@dataclass
class Supplier:
    """Supplier model."""
    id: str
    name: str
    contact_email: str
    contact_phone: str
    address: str
    lead_time_days: int  # Average delivery time
    reliability_score: float = 1.0  # 0-1 score
    products: List[str] = field(default_factory=list)  # Product IDs
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'lead_time_days': self.lead_time_days,
            'reliability_score': self.reliability_score,
            'products': self.products,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Supplier':
        return cls(
            id=data['id'],
            name=data['name'],
            contact_email=data.get('contact_email', ''),
            contact_phone=data.get('contact_phone', ''),
            address=data.get('address', ''),
            lead_time_days=data.get('lead_time_days', 7),
            reliability_score=data.get('reliability_score', 1.0),
            products=data.get('products', [])
        )


@dataclass(unsafe_hash=True)
class Alert:
    """Alert model for notifications."""
    id: str
    product_id: str
    alert_type: str  # 'low_stock', 'out_of_stock', 'reorder', 'overstock'
    severity: AlertSeverity
    message: str
    quantity: int
    threshold: int
    created_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    acknowledged_at: Optional[datetime] = None
    
    @property
    def priority_score(self) -> int:
        """Priority score for heap ordering (lower = higher priority)."""
        severity_scores = {
            AlertSeverity.CRITICAL: 0,
            AlertSeverity.HIGH: 1,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.LOW: 3
        }
        return severity_scores.get(self.severity, 3)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'product_id': self.product_id,
            'alert_type': self.alert_type,
            'severity': self.severity.value,
            'message': self.message,
            'quantity': self.quantity,
            'threshold': self.threshold,
            'created_at': self.created_at.isoformat(),
            'acknowledged': self.acknowledged,
            'priority_score': self.priority_score
        }


@dataclass
class InventorySummary:
    """Inventory summary statistics."""
    total_products: int
    total_quantity: int
    total_value: float
    low_stock_count: int
    out_of_stock_count: int
    pending_orders: int
    total_sales: int
    total_revenue: float
    categories: Dict[str, int]
    top_selling: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_products': self.total_products,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'low_stock_count': self.low_stock_count,
            'out_of_stock_count': self.out_of_stock_count,
            'pending_orders': self.pending_orders,
            'total_sales': self.total_sales,
            'total_revenue': self.total_revenue,
            'categories': self.categories,
            'top_selling': self.top_selling
        }
