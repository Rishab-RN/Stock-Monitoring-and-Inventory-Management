"""
Binary Heap Implementation (Min-Heap and Max-Heap)
==================================================
Time Complexity:
- Insert (push): O(log n)
- Extract (pop): O(log n)
- Peek (top): O(1)
- Heapify: O(n)

Space Complexity: O(n)

Used for:
- Low stock alerts (Min-Heap by quantity)
- Top sellers ranking (Max-Heap by sales)
- Priority-based order processing
"""

from typing import Any, List, Optional, Callable, Tuple


class MinHeap:
    """
    Min-Heap implementation using array representation.
    
    Parent at index i has:
    - Left child at 2i + 1
    - Right child at 2i + 2
    - Parent at (i - 1) // 2
    """
    
    def __init__(self, key_func: Callable[[Any], Any] = None):
        """
        Initialize MinHeap.
        
        Args:
            key_func: Function to extract comparison key from items
        """
        self.heap: List[Any] = []
        self.key_func = key_func or (lambda x: x)
    
    def _parent(self, i: int) -> int:
        """Get parent index. O(1)."""
        return (i - 1) // 2
    
    def _left_child(self, i: int) -> int:
        """Get left child index. O(1)."""
        return 2 * i + 1
    
    def _right_child(self, i: int) -> int:
        """Get right child index. O(1)."""
        return 2 * i + 2
    
    def _swap(self, i: int, j: int) -> None:
        """Swap elements at indices i and j. O(1)."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _compare(self, a: Any, b: Any) -> bool:
        """Compare using key function. Returns True if a < b."""
        return self.key_func(a) < self.key_func(b)
    
    def _sift_up(self, i: int) -> None:
        """
        Move element up to restore heap property.
        
        Time Complexity: O(log n)
        """
        while i > 0:
            parent = self._parent(i)
            if self._compare(self.heap[i], self.heap[parent]):
                self._swap(i, parent)
                i = parent
            else:
                break
    
    def _sift_down(self, i: int) -> None:
        """
        Move element down to restore heap property.
        
        Time Complexity: O(log n)
        """
        n = len(self.heap)
        while True:
            smallest = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            if left < n and self._compare(self.heap[left], self.heap[smallest]):
                smallest = left
            if right < n and self._compare(self.heap[right], self.heap[smallest]):
                smallest = right
            
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break
    
    def push(self, item: Any) -> None:
        """
        Insert an item into the heap.
        
        Time Complexity: O(log n)
        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
    
    def pop(self) -> Optional[Any]:
        """
        Remove and return the minimum element.
        
        Time Complexity: O(log n)
        """
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        
        return min_item
    
    def peek(self) -> Optional[Any]:
        """
        Return minimum element without removing.
        
        Time Complexity: O(1)
        """
        return self.heap[0] if self.heap else None
    
    def heapify(self, items: List[Any]) -> None:
        """
        Build heap from a list of items.
        
        Time Complexity: O(n) - more efficient than n insertions
        """
        self.heap = items.copy()
        # Start from last non-leaf and sift down
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)
    
    def __len__(self) -> int:
        return len(self.heap)
    
    def __bool__(self) -> bool:
        return len(self.heap) > 0
    
    def __repr__(self) -> str:
        return f"MinHeap({self.heap})"


class MaxHeap:
    """
    Max-Heap implementation.
    
    Uses MinHeap internally by negating keys.
    """
    
    def __init__(self, key_func: Callable[[Any], Any] = None):
        """Initialize MaxHeap with optional key function."""
        self._key_func = key_func or (lambda x: x)
        # Negate the key for max-heap behavior
        self._heap = MinHeap(key_func=lambda x: -self._key_func(x))
    
    def push(self, item: Any) -> None:
        """Insert item. O(log n)."""
        self._heap.push(item)
    
    def pop(self) -> Optional[Any]:
        """Remove and return maximum. O(log n)."""
        return self._heap.pop()
    
    def peek(self) -> Optional[Any]:
        """Return maximum without removing. O(1)."""
        return self._heap.peek()
    
    def heapify(self, items: List[Any]) -> None:
        """Build heap from list. O(n)."""
        self._heap.heapify(items)
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __bool__(self) -> bool:
        return bool(self._heap)
    
    def __repr__(self) -> str:
        return f"MaxHeap({self._heap.heap})"


class PriorityQueue:
    """
    Priority Queue implementation using Min-Heap.
    
    Items with lower priority values are dequeued first.
    Supports priority updates and item tracking.
    """
    
    def __init__(self):
        """Initialize empty priority queue."""
        self.heap: List[Tuple[int, int, Any]] = []  # (priority, counter, item)
        self.counter = 0  # Unique sequence count for tie-breaking
        self.entry_finder = {}  # Map item to entry
        self.REMOVED = '<removed>'
    
    def push(self, item: Any, priority: int = 0) -> None:
        """
        Add item with priority or update existing priority.
        
        Time Complexity: O(log n)
        """
        if item in self.entry_finder:
            self.remove(item)
        
        entry = [priority, self.counter, item]
        self.entry_finder[item] = entry
        self.counter += 1
        
        self.heap.append(entry)
        self._sift_up(len(self.heap) - 1)
    
    def remove(self, item: Any) -> None:
        """Mark an existing item as removed. O(1)."""
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED
    
    def pop(self) -> Optional[Any]:
        """
        Remove and return the lowest priority item.
        
        Time Complexity: O(log n)
        """
        while self.heap:
            priority, count, item = self._pop_entry()
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item
        return None
    
    def peek(self) -> Optional[Tuple[Any, int]]:
        """
        Return (item, priority) of lowest priority item.
        
        Time Complexity: O(1)
        """
        while self.heap:
            priority, count, item = self.heap[0]
            if item is not self.REMOVED:
                return (item, priority)
            self._pop_entry()
        return None
    
    def _sift_up(self, i: int) -> None:
        """Restore heap property upward. O(log n)."""
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] < self.heap[parent][0]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break
    
    def _sift_down(self, i: int) -> None:
        """Restore heap property downward. O(log n)."""
        n = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            
            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break
    
    def _pop_entry(self) -> Tuple[int, int, Any]:
        """Remove and return root entry. O(log n)."""
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root
    
    def update_priority(self, item: Any, new_priority: int) -> None:
        """Update priority of an existing item. O(log n)."""
        self.push(item, new_priority)
    
    def __len__(self) -> int:
        return len(self.entry_finder)
    
    def __bool__(self) -> bool:
        return bool(self.entry_finder)
    
    def __contains__(self, item: Any) -> bool:
        return item in self.entry_finder
    
    def __repr__(self) -> str:
        items = [(item, entry[0]) for item, entry in self.entry_finder.items()]
        return f"PriorityQueue({items})"
