"""
Graph Implementation for Supplier Network
==========================================
Time Complexity:
- Add Vertex: O(1)
- Add Edge: O(1)
- BFS/DFS: O(V + E)
- Dijkstra: O((V + E) log V)
- Find Path: O(V + E)

Space Complexity: O(V + E)

Used for:
- Supplier-product relationships
- Finding alternative suppliers
- Supply chain optimization
- Risk analysis (centrality metrics)
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from collections import deque
import heapq


class Graph:
    """
    Weighted directed graph using adjacency list representation.
    
    Features:
    - Weighted edges for cost/distance
    - BFS and DFS traversals
    - Shortest path (Dijkstra)
    - Cycle detection
    - Centrality metrics
    """
    
    def __init__(self, directed: bool = True):
        """
        Initialize graph.
        
        Args:
            directed: If True, edges are one-way
        """
        self.directed = directed
        self.vertices: Dict[str, Any] = {}  # vertex_id -> vertex_data
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {}  # vertex_id -> [(neighbor, weight)]
        self.edge_count = 0
    
    def add_vertex(self, vertex_id: str, data: Any = None) -> bool:
        """
        Add a vertex to the graph.
        
        Time Complexity: O(1)
        
        Returns:
            True if vertex was added, False if already exists
        """
        if vertex_id in self.vertices:
            return False
        
        self.vertices[vertex_id] = data
        self.adjacency[vertex_id] = []
        return True
    
    def add_edge(self, from_vertex: str, to_vertex: str, weight: float = 1.0) -> bool:
        """
        Add an edge between vertices.
        
        Time Complexity: O(1)
        
        Args:
            from_vertex: Source vertex ID
            to_vertex: Destination vertex ID
            weight: Edge weight (default 1.0)
            
        Returns:
            True if edge was added
        """
        # Auto-add vertices if they don't exist
        if from_vertex not in self.vertices:
            self.add_vertex(from_vertex)
        if to_vertex not in self.vertices:
            self.add_vertex(to_vertex)
        
        self.adjacency[from_vertex].append((to_vertex, weight))
        self.edge_count += 1
        
        if not self.directed:
            self.adjacency[to_vertex].append((from_vertex, weight))
            self.edge_count += 1
        
        return True
    
    def remove_vertex(self, vertex_id: str) -> bool:
        """
        Remove a vertex and all its edges.
        
        Time Complexity: O(V + E)
        """
        if vertex_id not in self.vertices:
            return False
        
        # Remove all edges to this vertex
        for adj_list in self.adjacency.values():
            adj_list[:] = [(v, w) for v, w in adj_list if v != vertex_id]
        
        del self.vertices[vertex_id]
        del self.adjacency[vertex_id]
        return True
    
    def remove_edge(self, from_vertex: str, to_vertex: str) -> bool:
        """
        Remove an edge between vertices.
        
        Time Complexity: O(degree of from_vertex)
        """
        if from_vertex not in self.adjacency:
            return False
        
        original_len = len(self.adjacency[from_vertex])
        self.adjacency[from_vertex] = [
            (v, w) for v, w in self.adjacency[from_vertex] if v != to_vertex
        ]
        
        if len(self.adjacency[from_vertex]) < original_len:
            self.edge_count -= 1
            if not self.directed:
                self.adjacency[to_vertex] = [
                    (v, w) for v, w in self.adjacency[to_vertex] if v != from_vertex
                ]
                self.edge_count -= 1
            return True
        return False
    
    def get_neighbors(self, vertex_id: str) -> List[Tuple[str, float]]:
        """Get all neighbors with edge weights. O(1)."""
        return self.adjacency.get(vertex_id, [])
    
    def bfs(self, start: str) -> List[str]:
        """
        Breadth-First Search traversal.
        
        Time Complexity: O(V + E)
        
        Returns:
            List of vertices in BFS order
        """
        if start not in self.vertices:
            return []
        
        visited = set()
        result = []
        queue = deque([start])
        visited.add(start)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in self.adjacency[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start: str) -> List[str]:
        """
        Depth-First Search traversal.
        
        Time Complexity: O(V + E)
        
        Returns:
            List of vertices in DFS order
        """
        if start not in self.vertices:
            return []
        
        visited = set()
        result = []
        
        def _dfs(vertex: str):
            visited.add(vertex)
            result.append(vertex)
            for neighbor, _ in self.adjacency[vertex]:
                if neighbor not in visited:
                    _dfs(neighbor)
        
        _dfs(start)
        return result
    
    def dijkstra(self, start: str) -> Dict[str, Tuple[float, List[str]]]:
        """
        Dijkstra's shortest path algorithm.
        
        Time Complexity: O((V + E) log V)
        
        Returns:
            Dict mapping vertex -> (distance, path)
        """
        if start not in self.vertices:
            return {}
        
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0
        parents = {start: None}
        
        # Priority queue: (distance, vertex)
        pq = [(0, start)]
        visited = set()
        
        while pq:
            dist, vertex = heapq.heappop(pq)
            
            if vertex in visited:
                continue
            visited.add(vertex)
            
            for neighbor, weight in self.adjacency[vertex]:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parents[neighbor] = vertex
                    heapq.heappush(pq, (new_dist, neighbor))
        
        # Build result with paths
        result = {}
        for vertex in self.vertices:
            if distances[vertex] < float('inf'):
                path = []
                current = vertex
                while current is not None:
                    path.append(current)
                    current = parents.get(current)
                result[vertex] = (distances[vertex], path[::-1])
        
        return result
    
    def find_path(self, start: str, end: str) -> Optional[List[str]]:
        """
        Find any path between two vertices using BFS.
        
        Time Complexity: O(V + E)
        """
        if start not in self.vertices or end not in self.vertices:
            return None
        
        if start == end:
            return [start]
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor, _ in self.adjacency[vertex]:
                if neighbor == end:
                    return path + [end]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def shortest_path(self, start: str, end: str) -> Optional[Tuple[float, List[str]]]:
        """
        Find shortest weighted path between vertices.
        
        Time Complexity: O((V + E) log V)
        
        Returns:
            (distance, path) or None if no path exists
        """
        result = self.dijkstra(start)
        return result.get(end)
    
    def has_cycle(self) -> bool:
        """
        Detect if graph has a cycle.
        
        Time Complexity: O(V + E)
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in self.vertices}
        
        def has_cycle_dfs(vertex: str) -> bool:
            color[vertex] = GRAY
            for neighbor, _ in self.adjacency[vertex]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and has_cycle_dfs(neighbor):
                    return True
            color[vertex] = BLACK
            return False
        
        for vertex in self.vertices:
            if color[vertex] == WHITE:
                if has_cycle_dfs(vertex):
                    return True
        return False
    
    def topological_sort(self) -> Optional[List[str]]:
        """
        Topological ordering (DAG only).
        
        Time Complexity: O(V + E)
        
        Returns:
            Sorted list or None if cycle exists
        """
        if self.has_cycle():
            return None
        
        in_degree = {v: 0 for v in self.vertices}
        for adj_list in self.adjacency.values():
            for neighbor, _ in adj_list:
                in_degree[neighbor] += 1
        
        queue = deque([v for v, d in in_degree.items() if d == 0])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            for neighbor, _ in self.adjacency[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    def degree_centrality(self) -> Dict[str, float]:
        """
        Calculate degree centrality for each vertex.
        
        High centrality = important node (many connections)
        
        Returns:
            Dict mapping vertex -> centrality score (0-1)
        """
        n = len(self.vertices)
        if n <= 1:
            return {v: 0.0 for v in self.vertices}
        
        result = {}
        for vertex in self.vertices:
            degree = len(self.adjacency[vertex])
            if not self.directed:
                # Count only once for undirected
                result[vertex] = degree / (n - 1)
            else:
                # Out-degree centrality
                result[vertex] = degree / (n - 1)
        
        return result
    
    def get_connected_components(self) -> List[Set[str]]:
        """
        Find all connected components.
        
        Time Complexity: O(V + E)
        """
        visited = set()
        components = []
        
        for vertex in self.vertices:
            if vertex not in visited:
                component = set()
                queue = deque([vertex])
                while queue:
                    v = queue.popleft()
                    if v not in visited:
                        visited.add(v)
                        component.add(v)
                        for neighbor, _ in self.adjacency[v]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                components.append(component)
        
        return components
    
    def to_dict(self) -> dict:
        """Convert graph to dictionary for JSON serialization."""
        return {
            "directed": self.directed,
            "vertices": {v: self.vertices[v] for v in self.vertices},
            "edges": [
                {"from": v, "to": n, "weight": w}
                for v in self.adjacency
                for n, w in self.adjacency[v]
            ]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Graph':
        """Create graph from dictionary."""
        graph = cls(directed=data.get("directed", True))
        for v, d in data.get("vertices", {}).items():
            graph.add_vertex(v, d)
        for edge in data.get("edges", []):
            graph.add_edge(edge["from"], edge["to"], edge.get("weight", 1.0))
        return graph
    
    def __len__(self) -> int:
        return len(self.vertices)
    
    def __repr__(self) -> str:
        return f"Graph(vertices={len(self.vertices)}, edges={self.edge_count}, directed={self.directed})"
