"""
AVL Tree Implementation for Range Queries
==========================================
Time Complexity:
- Insert: O(log n)
- Delete: O(log n)
- Search: O(log n)
- Range Query: O(log n + k) where k is result size

Space Complexity: O(n)

AVL Tree is a self-balancing BST where the heights of two child
subtrees differ by at most one (balance factor ∈ {-1, 0, 1}).
"""

from typing import Any, Optional, List, Tuple, Callable


class AVLNode:
    """Node for AVL Tree storing key-value pairs."""
    
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1


class AVLTree:
    """
    Self-balancing AVL Tree implementation.
    
    Features:
    - Automatic balancing after insertions/deletions
    - Efficient range queries for price/quantity filtering
    - In-order traversal for sorted access
    """
    
    def __init__(self, key_func: Callable[[Any], Any] = None):
        """
        Initialize AVL Tree.
        
        Args:
            key_func: Optional function to extract comparison key from values
        """
        self.root: Optional[AVLNode] = None
        self.size = 0
        self.key_func = key_func or (lambda x: x)
    
    def _height(self, node: Optional[AVLNode]) -> int:
        """Get height of node. O(1)."""
        return node.height if node else 0
    
    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculate balance factor (left height - right height).
        
        Balance factor in {-1, 0, 1} means balanced.
        """
        return self._height(node.left) - self._height(node.right)
    
    def _update_height(self, node: AVLNode) -> None:
        """Update node height based on children. O(1)."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Right rotation for rebalancing.
        
              y                x
             / \              / \
            x   C    -->     A   y
           / \                  / \
          A   B                B   C
          
        Time Complexity: O(1)
        """
        x = y.left
        B = x.right
        
        x.right = y
        y.left = B
        
        self._update_height(y)
        self._update_height(x)
        
        return x
    
    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """
        Left rotation for rebalancing.
        
            x                  y
           / \                / \
          A   y     -->      x   C
             / \            / \
            B   C          A   B
            
        Time Complexity: O(1)
        """
        y = x.right
        B = y.left
        
        y.left = x
        x.right = B
        
        self._update_height(x)
        self._update_height(y)
        
        return y
    
    def _insert(self, node: Optional[AVLNode], key: Any, value: Any) -> AVLNode:
        """
        Recursive insert with rebalancing.
        
        Time Complexity: O(log n)
        """
        # Standard BST insert
        if not node:
            self.size += 1
            return AVLNode(key, value)
        
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # Update existing value
            node.value = value
            return node
        
        # Update height
        self._update_height(node)
        
        # Get balance factor and rebalance if needed
        balance = self._balance_factor(node)
        
        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        
        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def insert(self, key: Any, value: Any) -> None:
        """
        Insert a key-value pair into the AVL Tree.
        
        Time Complexity: O(log n)
        """
        self.root = self._insert(self.root, key, value)
    
    def _min_node(self, node: AVLNode) -> AVLNode:
        """Find minimum node in subtree. O(log n)."""
        current = node
        while current.left:
            current = current.left
        return current
    
    def _delete(self, node: Optional[AVLNode], key: Any) -> Optional[AVLNode]:
        """
        Recursive delete with rebalancing.
        
        Time Complexity: O(log n)
        """
        if not node:
            return None
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node found - handle deletion
            if not node.left:
                self.size -= 1
                return node.right
            elif not node.right:
                self.size -= 1
                return node.left
            
            # Two children: get inorder successor
            successor = self._min_node(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete(node.right, successor.key)
        
        # Update height and rebalance
        self._update_height(node)
        balance = self._balance_factor(node)
        
        # Left Left Case
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        
        # Left Right Case
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        
        # Right Left Case
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def delete(self, key: Any) -> bool:
        """
        Delete a key from the AVL Tree.
        
        Time Complexity: O(log n)
        
        Returns:
            True if key was found and deleted
        """
        old_size = self.size
        self.root = self._delete(self.root, key)
        return self.size < old_size
    
    def _search(self, node: Optional[AVLNode], key: Any) -> Optional[Any]:
        """Recursive search. O(log n)."""
        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the AVL Tree.
        
        Time Complexity: O(log n)
        """
        return self._search(self.root, key)
    
    def _range_query(self, node: Optional[AVLNode], low: Any, high: Any, result: List) -> None:
        """
        Recursive range query.
        
        Time Complexity: O(log n + k) where k is the number of results
        """
        if not node:
            return
        
        # If node key is greater than low, check left subtree
        if node.key > low:
            self._range_query(node.left, low, high, result)
        
        # Include node if in range
        if low <= node.key <= high:
            result.append((node.key, node.value))
        
        # If node key is less than high, check right subtree
        if node.key < high:
            self._range_query(node.right, low, high, result)
    
    def range_query(self, low: Any, high: Any) -> List[Tuple[Any, Any]]:
        """
        Find all key-value pairs where low <= key <= high.
        
        Time Complexity: O(log n + k) where k is the result size
        
        Args:
            low: Lower bound (inclusive)
            high: Upper bound (inclusive)
            
        Returns:
            List of (key, value) tuples in the range
        """
        result = []
        self._range_query(self.root, low, high, result)
        return result
    
    def _inorder(self, node: Optional[AVLNode], result: List) -> None:
        """Inorder traversal for sorted output. O(n)."""
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)
    
    def inorder(self) -> List[Tuple[Any, Any]]:
        """
        Return all entries in sorted order.
        
        Time Complexity: O(n)
        """
        result = []
        self._inorder(self.root, result)
        return result
    
    def min(self) -> Optional[Tuple[Any, Any]]:
        """Get minimum key-value pair. O(log n)."""
        if not self.root:
            return None
        node = self._min_node(self.root)
        return (node.key, node.value)
    
    def max(self) -> Optional[Tuple[Any, Any]]:
        """Get maximum key-value pair. O(log n)."""
        if not self.root:
            return None
        current = self.root
        while current.right:
            current = current.right
        return (current.key, current.value)
    
    def __len__(self) -> int:
        """Return number of elements. O(1)."""
        return self.size
    
    def __contains__(self, key: Any) -> bool:
        """Check if key exists. O(log n)."""
        return self.search(key) is not None
    
    def __repr__(self) -> str:
        """String representation."""
        items = [f"{k}: {v}" for k, v in self.inorder()]
        return f"AVLTree({{{', '.join(items)}}})"
