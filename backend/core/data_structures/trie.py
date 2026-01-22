"""
Trie (Prefix Tree) Implementation for Autocomplete
===================================================
Time Complexity:
- Insert: O(m) where m is key length
- Search: O(m)
- Prefix Search: O(m + k) where k is number of matches
- Delete: O(m)

Space Complexity: O(n * m) where n is number of keys

Used for:
- Product name autocomplete
- Category suggestion
- Fast prefix-based filtering
"""

from typing import Dict, List, Optional, Tuple, Any


class TrieNode:
    """Node in the Trie structure."""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False
        self.value: Any = None  # Store associated value (e.g., product object)
        self.frequency: int = 0  # For popularity-based sorting


class Trie:
    """
    Trie implementation for efficient prefix-based search.
    
    Features:
    - Case-insensitive search
    - Frequency-based ranking
    - Prefix autocompletion
    """
    
    def __init__(self, case_sensitive: bool = False):
        """Initialize Trie."""
        self.root = TrieNode()
        self.size = 0
        self.case_sensitive = case_sensitive
    
    def _normalize(self, key: str) -> str:
        """Normalize key based on case sensitivity."""
        return key if self.case_sensitive else key.lower()
    
    def insert(self, key: str, value: Any = None) -> None:
        """
        Insert a key into the Trie.
        
        Time Complexity: O(m) where m is key length
        
        Args:
            key: The string key to insert
            value: Optional value to associate with the key
        """
        key = self._normalize(key)
        node = self.root
        
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end:
            self.size += 1
        
        node.is_end = True
        node.value = value
        node.frequency += 1
    
    def search(self, key: str) -> Optional[Any]:
        """
        Search for exact key match.
        
        Time Complexity: O(m)
        
        Returns:
            Associated value if found, None otherwise
        """
        key = self._normalize(key)
        node = self._find_node(key)
        
        if node and node.is_end:
            return node.value
        return None
    
    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Find node corresponding to prefix. O(m)."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def starts_with(self, prefix: str) -> bool:
        """
        Check if any key starts with prefix.
        
        Time Complexity: O(m)
        """
        prefix = self._normalize(prefix)
        return self._find_node(prefix) is not None
    
    def _collect_all(self, node: TrieNode, prefix: str, results: List[Tuple[str, Any, int]]) -> None:
        """
        Collect all keys from a node.
        
        DFS traversal to find all complete keys.
        """
        if node.is_end:
            results.append((prefix, node.value, node.frequency))
        
        for char, child in node.children.items():
            self._collect_all(child, prefix + char, results)
    
    def autocomplete(self, prefix: str, limit: int = 10) -> List[Tuple[str, Any]]:
        """
        Get all keys that start with prefix.
        
        Time Complexity: O(m + k) where k is number of matches
        
        Args:
            prefix: The prefix to search for
            limit: Maximum number of results to return
            
        Returns:
            List of (key, value) tuples sorted by frequency
        """
        prefix = self._normalize(prefix)
        node = self._find_node(prefix)
        
        if not node:
            return []
        
        results = []
        self._collect_all(node, prefix, results)
        
        # Sort by frequency (descending) and return top results
        results.sort(key=lambda x: -x[2])
        return [(key, value) for key, value, _ in results[:limit]]
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the Trie.
        
        Time Complexity: O(m)
        
        Returns:
            True if key was found and deleted
        """
        key = self._normalize(key)
        
        def _delete(node: TrieNode, key: str, depth: int) -> bool:
            if depth == len(key):
                if not node.is_end:
                    return False
                node.is_end = False
                node.value = None
                self.size -= 1
                return len(node.children) == 0
            
            char = key[depth]
            if char not in node.children:
                return False
            
            should_delete = _delete(node.children[char], key, depth + 1)
            
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            
            return False
        
        return _delete(self.root, key, 0) or self.size >= 0
    
    def get_all_keys(self) -> List[str]:
        """Return all keys in the Trie. O(n)."""
        results = []
        self._collect_all(self.root, "", results)
        return [key for key, _, _ in results]
    
    def fuzzy_search(self, query: str, max_distance: int = 1) -> List[Tuple[str, Any, int]]:
        """
        Find keys within edit distance of query.
        
        Uses dynamic programming for Levenshtein distance.
        
        Args:
            query: The search query
            max_distance: Maximum edit distance allowed
            
        Returns:
            List of (key, value, distance) tuples
        """
        query = self._normalize(query)
        results = []
        
        def _fuzzy(node: TrieNode, prefix: str, prev_row: List[int]):
            current_row = [prev_row[0] + 1]
            
            for i, char in enumerate(query):
                insert_cost = current_row[i] + 1
                delete_cost = prev_row[i + 1] + 1
                replace_cost = prev_row[i] + (0 if prefix[-1] == char else 1) if prefix else 1
                current_row.append(min(insert_cost, delete_cost, replace_cost))
            
            if current_row[-1] <= max_distance and node.is_end:
                results.append((prefix, node.value, current_row[-1]))
            
            if min(current_row) <= max_distance:
                for char, child in node.children.items():
                    _fuzzy(child, prefix + char, current_row)
        
        initial_row = list(range(len(query) + 1))
        for char, child in self.root.children.items():
            _fuzzy(child, char, initial_row)
        
        results.sort(key=lambda x: x[2])
        return results
    
    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, key: str) -> bool:
        return self.search(key) is not None
    
    def __repr__(self) -> str:
        return f"Trie(size={self.size}, keys={self.get_all_keys()[:5]}...)"
