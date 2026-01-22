"""
Custom HashMap Implementation with Chaining
============================================
Time Complexity:
- Insert: O(1) average, O(n) worst case
- Delete: O(1) average, O(n) worst case  
- Search: O(1) average, O(n) worst case

Space Complexity: O(n)

This implementation uses separate chaining for collision resolution
and dynamic resizing when load factor exceeds threshold.
"""

from typing import Any, Optional, List, Tuple, Iterator


class HashNode:
    """Node for storing key-value pairs in the chain."""
    
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.next: Optional['HashNode'] = None


class HashMap:
    """
    Custom HashMap implementation using separate chaining.
    
    Features:
    - Dynamic resizing when load factor > 0.75
    - Consistent hashing for uniform distribution
    - Support for any hashable key type
    """
    
    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.75
    
    def __init__(self, capacity: int = INITIAL_CAPACITY):
        """Initialize HashMap with given capacity."""
        self.capacity = capacity
        self.size = 0
        self.buckets: List[Optional[HashNode]] = [None] * capacity
        
    def _hash(self, key: Any) -> int:
        """
        Compute hash index for a key.
        Uses Python's built-in hash with modulo for bucket index.
        
        Time Complexity: O(1)
        """
        return hash(key) % self.capacity
    
    def _resize(self) -> None:
        """
        Double the capacity and rehash all entries.
        Called when load factor exceeds threshold.
        
        Time Complexity: O(n)
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        
        # Rehash all existing entries
        for bucket in old_buckets:
            current = bucket
            while current:
                self.put(current.key, current.value)
                current = current.next
    
    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update a key-value pair.
        
        Time Complexity: O(1) average, O(n) worst case
        
        Args:
            key: The key to insert
            value: The value associated with the key
        """
        # Check if resize needed
        if self.size / self.capacity > self.LOAD_FACTOR_THRESHOLD:
            self._resize()
            
        index = self._hash(key)
        
        # Check if key already exists and update
        current = self.buckets[index]
        while current:
            if current.key == key:
                current.value = value  # Update existing
                return
            current = current.next
        
        # Insert new node at head of chain
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1
    
    def get(self, key: Any, default: Any = None) -> Any:
        """
        Retrieve value for a key.
        
        Time Complexity: O(1) average, O(n) worst case
        
        Args:
            key: The key to search for
            default: Value to return if key not found
            
        Returns:
            Value associated with key, or default if not found
        """
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
            
        return default
    
    def remove(self, key: Any) -> bool:
        """
        Remove a key-value pair.
        
        Time Complexity: O(1) average, O(n) worst case
        
        Args:
            key: The key to remove
            
        Returns:
            True if key was found and removed, False otherwise
        """
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
            
        return False
    
    def contains(self, key: Any) -> bool:
        """Check if key exists in HashMap. O(1) average."""
        return self.get(key) is not None
    
    def keys(self) -> List[Any]:
        """Return all keys in the HashMap. O(n)."""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.key)
                current = current.next
        return result
    
    def values(self) -> List[Any]:
        """Return all values in the HashMap. O(n)."""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.value)
                current = current.next
        return result
    
    def items(self) -> List[Tuple[Any, Any]]:
        """Return all key-value pairs. O(n)."""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append((current.key, current.value))
                current = current.next
        return result
    
    def __len__(self) -> int:
        """Return number of entries. O(1)."""
        return self.size
    
    def __contains__(self, key: Any) -> bool:
        """Support 'in' operator. O(1) average."""
        return self.contains(key)
    
    def __getitem__(self, key: Any) -> Any:
        """Support bracket notation for get. O(1) average."""
        value = self.get(key)
        if value is None and key not in self:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """Support bracket notation for set. O(1) average."""
        self.put(key, value)
    
    def __delitem__(self, key: Any) -> None:
        """Support del operator. O(1) average."""
        if not self.remove(key):
            raise KeyError(key)
    
    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys. O(n)."""
        return iter(self.keys())
    
    def __repr__(self) -> str:
        """String representation of HashMap."""
        items = [f"{k}: {v}" for k, v in self.items()]
        return "HashMap({" + ", ".join(items) + "})"
    
    def load_factor(self) -> float:
        """Return current load factor."""
        return self.size / self.capacity
    
    def get_stats(self) -> dict:
        """Return statistics about the HashMap."""
        chain_lengths = []
        for bucket in self.buckets:
            length = 0
            current = bucket
            while current:
                length += 1
                current = current.next
            chain_lengths.append(length)
        
        return {
            "size": self.size,
            "capacity": self.capacity,
            "load_factor": self.load_factor(),
            "max_chain_length": max(chain_lengths) if chain_lengths else 0,
            "avg_chain_length": sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0,
            "empty_buckets": chain_lengths.count(0)
        }
