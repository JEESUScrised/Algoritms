from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set
import heapq


class TransportGraph:
    
    def __init__(self):
        self.stations: Set[str] = set()
        self.graph: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.edges: List[Tuple[str, str, float]] = []
        self.station_index: Dict[str, int] = {}
        self.index_station: Dict[int, str] = {}
    
    def add_station(self, name: str):
        self.stations.add(name)
        if name not in self.station_index:
            idx = len(self.station_index)
            self.station_index[name] = idx
            self.index_station[idx] = name
    
    def add_route(self, from_station: str, to_station: str, weight: float):
        self.add_station(from_station)
        self.add_station(to_station)
        self.graph[from_station].append((to_station, weight))
        self.edges.append((from_station, to_station, weight))
    
    def shortest_path_Dijkstra(self, start: str) -> Dict[str, float]:
        if start not in self.stations:
            return {}
        
        distances = {station: float('inf') for station in self.stations}
        distances[start] = 0.0
        visited = set()
        heap = [(0.0, start)]
        
        while heap:
            current_dist, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor, weight in self.graph[current]:
                if neighbor in visited:
                    continue
                
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))
        
        return distances
    
    def shortest_path_BellmanFord(self, start: str) -> Tuple[Dict[str, float], bool]:
        if start not in self.stations:
            return {}, False
        
        distances = {station: float('inf') for station in self.stations}
        distances[start] = 0.0
        
        for _ in range(len(self.stations) - 1):
            for from_station, to_station, weight in self.edges:
                if distances[from_station] != float('inf'):
                    new_dist = distances[from_station] + weight
                    if new_dist < distances[to_station]:
                        distances[to_station] = new_dist
        
        has_negative_cycle = False
        for from_station, to_station, weight in self.edges:
            if distances[from_station] != float('inf'):
                if distances[from_station] + weight < distances[to_station]:
                    has_negative_cycle = True
                    break
        
        return distances, has_negative_cycle
    
    def all_pairs_shortest_paths_FloydWarshall(self) -> List[List[float]]:
        n = len(self.stations)
        if n == 0:
            return []
        
        dist = [[float('inf') for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            dist[i][i] = 0.0
        
        for from_station, to_station, weight in self.edges:
            from_idx = self.station_index[from_station]
            to_idx = self.station_index[to_station]
            dist[from_idx][to_idx] = weight
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
        
        return dist
    
    def get_station_name(self, index: int) -> str:
        return self.index_station.get(index, "")
    
    def get_all_stations(self) -> List[str]:
        return sorted(list(self.stations))


class NetworkOptimizer:
    
    def __init__(self, graph: TransportGraph):
        self.graph = graph
    
    def minimum_spanning_tree_Kruskal(self) -> Tuple[List[Tuple[str, str, float]], float]:
        edges = sorted(self.graph.edges, key=lambda x: x[2])
        
        parent = {station: station for station in self.graph.stations}
        rank = {station: 0 for station in self.graph.stations}
        
        def find(x: str) -> str:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x: str, y: str):
            root_x = find(x)
            root_y = find(y)
            
            if root_x == root_y:
                return False
            
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1
            
            return True
        
        mst_edges = []
        total_weight = 0.0
        
        for from_station, to_station, weight in edges:
            if find(from_station) != find(to_station):
                if union(from_station, to_station):
                    mst_edges.append((from_station, to_station, weight))
                    total_weight += weight
        
        return mst_edges, total_weight
    
    def minimum_spanning_tree_Prim(self, start: Optional[str] = None) -> Tuple[List[Tuple[str, str, float]], float]:
        if not self.graph.stations:
            return [], 0.0
        
        if start is None:
            start = next(iter(self.graph.stations))
        
        if start not in self.graph.stations:
            return [], 0.0
        
        visited = {start}
        mst_edges = []
        total_weight = 0.0
        edges_heap = []
        
        for neighbor, weight in self.graph.graph[start]:
            heapq.heappush(edges_heap, (weight, start, neighbor))
        
        while len(visited) < len(self.graph.stations) and edges_heap:
            weight, from_station, to_station = heapq.heappop(edges_heap)
            
            if to_station in visited:
                continue
            
            visited.add(to_station)
            mst_edges.append((from_station, to_station, weight))
            total_weight += weight
            
            for neighbor, edge_weight in self.graph.graph[to_station]:
                if neighbor not in visited:
                    heapq.heappush(edges_heap, (edge_weight, to_station, neighbor))
        
        return mst_edges, total_weight
