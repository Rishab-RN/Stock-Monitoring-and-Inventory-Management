"""
Queue Implementations for Transaction Processing
=================================================
Time Complexity (all operations):
- Enqueue: O(1) amortized
- Dequeue: O(1)
- Peek: O(1)

Space Complexity: O(n)

Implementations:
1. CircularQueue - Fixed size ring buffer
2. DequeQueue - Double-ended queue
3. TransactionQueue - Specialized for inventory transactions
"""

from typing import Any, Optional, List, Generic, TypeVar
from collections import deque
from datetime import datetime
from dataclasses import dataclass, field


T = TypeVar('T')


class CircularQueue(Generic[T]):
    """
    Fixed-size circular queue (ring buffer).
    
    Memory efficient, no resizing needed.
    Good for bounded queues like recent transactions history.
    """
    
    def __init__(self, capacity: int):
        """
        Initialize circular queue with fixed capacity.
        
        Args:
            capacity: Maximum number of elements
        """
        self.capacity = capacity
        self.buffer: List[Optional[T]] = [None] * capacity
        self.head = 0  # Front index (for dequeue)
        self.tail = 0  # Back index (for enqueue)
        self.size = 0
    
    def enqueue(self, item: T) -> bool:
        """
        Add item to back of queue.
        
        Time Complexity: O(1)
        
        Returns:
            True if successful, False if full
        """
        if self.is_full():
            return False
        
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1
        return True
    
    def dequeue(self) -> Optional[T]:
        """
        Remove and return item from front.
        
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item
    
    def peek(self) -> Optional[T]:
        """Return front item without removing. O(1)."""
        return self.buffer[self.head] if not self.is_empty() else None
    
    def is_empty(self) -> bool:
        """Check if queue is empty. O(1)."""
        return self.size == 0
    
    def is_full(self) -> bool:
        """Check if queue is full. O(1)."""
        return self.size == self.capacity
    
    def __len__(self) -> int:
        return self.size
    
    def __repr__(self) -> str:
        items = []
        index = self.head
        for _ in range(self.size):
            items.append(self.buffer[index])
            index = (index + 1) % self.capacity
        return f"CircularQueue({items})"


class DequeQueue(Generic[T]):
    """
    Double-ended queue wrapper around collections.deque.
    
    Supports O(1) operations at both ends.
    Dynamically resizable.
    """
    
    def __init__(self, maxlen: Optional[int] = None):
        """
        Initialize deque-based queue.
        
        Args:
            maxlen: Optional maximum length (oldest items dropped if exceeded)
        """
        self._deque: deque = deque(maxlen=maxlen)
    
    def enqueue(self, item: T) -> None:
        """Add item to back. O(1)."""
        self._deque.append(item)
    
    def enqueue_front(self, item: T) -> None:
        """Add item to front (priority). O(1)."""
        self._deque.appendleft(item)
    
    def dequeue(self) -> Optional[T]:
        """Remove from front. O(1)."""
        return self._deque.popleft() if self._deque else None
    
    def dequeue_back(self) -> Optional[T]:
        """Remove from back. O(1)."""
        return self._deque.pop() if self._deque else None
    
    def peek(self) -> Optional[T]:
        """View front item. O(1)."""
        return self._deque[0] if self._deque else None
    
    def peek_back(self) -> Optional[T]:
        """View back item. O(1)."""
        return self._deque[-1] if self._deque else None
    
    def is_empty(self) -> bool:
        return len(self._deque) == 0
    
    def clear(self) -> None:
        """Remove all items. O(1)."""
        self._deque.clear()
    
    def to_list(self) -> List[T]:
        """Convert to list. O(n)."""
        return list(self._deque)
    
    def __len__(self) -> int:
        return len(self._deque)
    
    def __iter__(self):
        return iter(self._deque)
    
    def __repr__(self) -> str:
        return f"DequeQueue({list(self._deque)})"


@dataclass
class Transaction:
    """Transaction data structure."""
    id: str
    product_id: str
    transaction_type: str  # 'sale', 'restock', 'return', 'adjustment'
    quantity: int
    unit_price: float
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = 'pending'  # 'pending', 'processing', 'completed', 'failed'
    notes: str = ''
    
    @property
    def total_value(self) -> float:
        return self.quantity * self.unit_price
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'product_id': self.product_id,
            'type': self.transaction_type,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_value': self.total_value,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'notes': self.notes
        }


class TransactionQueue:
    """
    Specialized queue for inventory transactions.
    
    Features:
    - FIFO processing
    - Status tracking
    - Transaction history
    - Batch processing support
    """
    
    def __init__(self, history_size: int = 1000):
        """
        Initialize transaction queue.
        
        Args:
            history_size: Maximum number of completed transactions to keep
        """
        self.pending = DequeQueue[Transaction]()
        self.history = CircularQueue[Transaction](history_size)
        self.transaction_counter = 0
    
    def enqueue(self, product_id: str, transaction_type: str, 
                quantity: int, unit_price: float, notes: str = '') -> Transaction:
        """
        Create and queue a new transaction.
        
        Time Complexity: O(1)
        
        Returns:
            The created Transaction object
        """
        self.transaction_counter += 1
        transaction = Transaction(
            id=f"TXN-{self.transaction_counter:08d}",
            product_id=product_id,
            transaction_type=transaction_type,
            quantity=quantity,
            unit_price=unit_price,
            notes=notes
        )
        self.pending.enqueue(transaction)
        return transaction
    
    def dequeue(self) -> Optional[Transaction]:
        """
        Get next transaction for processing.
        
        Time Complexity: O(1)
        """
        transaction = self.pending.dequeue()
        if transaction:
            transaction.status = 'processing'
        return transaction
    
    def complete(self, transaction: Transaction, success: bool = True) -> None:
        """
        Mark a transaction as completed and add to history.
        
        Time Complexity: O(1)
        """
        transaction.status = 'completed' if success else 'failed'
        self.history.enqueue(transaction)
    
    def process_batch(self, handler, batch_size: int = 10) -> List[Transaction]:
        """
        Process multiple transactions.
        
        Args:
            handler: Function to process each transaction
            batch_size: Maximum transactions to process
            
        Returns:
            List of processed transactions
        """
        processed = []
        for _ in range(batch_size):
            transaction = self.dequeue()
            if not transaction:
                break
            
            try:
                handler(transaction)
                self.complete(transaction, success=True)
            except Exception as e:
                transaction.notes += f" [Error: {str(e)}]"
                self.complete(transaction, success=False)
            
            processed.append(transaction)
        
        return processed
    
    def peek_pending(self, n: int = 5) -> List[Transaction]:
        """View next n pending transactions. O(n)."""
        result = []
        for i, tx in enumerate(self.pending):
            if i >= n:
                break
            result.append(tx)
        return result
    
    def get_history(self, n: int = 50) -> List[Transaction]:
        """Get recent transaction history. O(n)."""
        result = []
        # Collect from circular buffer
        index = self.history.head
        for _ in range(min(n, self.history.size)):
            if self.history.buffer[index]:
                result.append(self.history.buffer[index])
            index = (index + 1) % self.history.capacity
        return result
    
    @property
    def pending_count(self) -> int:
        return len(self.pending)
    
    @property
    def history_count(self) -> int:
        return self.history.size
    
    def get_stats(self) -> dict:
        """Get queue statistics."""
        history_list = self.get_history(self.history_count)
        completed = [t for t in history_list if t.status == 'completed']
        failed = [t for t in history_list if t.status == 'failed']
        
        return {
            'pending': self.pending_count,
            'completed': len(completed),
            'failed': len(failed),
            'total_processed': len(history_list),
            'success_rate': len(completed) / len(history_list) if history_list else 1.0
        }
    
    def __repr__(self) -> str:
        return f"TransactionQueue(pending={self.pending_count}, history={self.history_count})"
