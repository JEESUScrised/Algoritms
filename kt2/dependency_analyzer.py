from collections import deque, defaultdict
from typing import List, Set, Dict, Optional, Tuple

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    nx = None
    plt = None


class DependencyGraph:
    
    def __init__(self):
        self.components: Set[str] = set()
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.reverse_graph: Dict[str, List[str]] = defaultdict(list)
        self.weights: Dict[Tuple[str, str], float] = {}
    
    def add_component(self, name: str):
        self.components.add(name)
        if name not in self.graph:
            self.graph[name] = []
        if name not in self.reverse_graph:
            self.reverse_graph[name] = []
    
    def add_dependency(self, from_component: str, to_component: str, weight: float = 1.0):
        self.add_component(from_component)
        self.add_component(to_component)
        
        if to_component not in self.graph[from_component]:
            self.graph[from_component].append(to_component)
        if from_component not in self.reverse_graph[to_component]:
            self.reverse_graph[to_component].append(from_component)
        
        self.weights[(from_component, to_component)] = weight
    
    def get_dependencies(self, component: str) -> List[str]:
        return self.graph.get(component, [])
    
    def is_acyclic(self) -> bool:
        in_degree = {comp: 0 for comp in self.components}
        for from_comp in self.graph:
            for to_comp in self.graph[from_comp]:
                in_degree[to_comp] += 1
        
        queue = deque([comp for comp in self.components if in_degree[comp] == 0])
        processed = 0
        
        while queue:
            current = queue.popleft()
            processed += 1
            
            for neighbor in self.graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return processed == len(self.components)
    
    def get_topological_order(self) -> Optional[List[str]]:
        if not self.is_acyclic():
            return None
        
        in_degree = {comp: 0 for comp in self.components}
        for from_comp in self.graph:
            for to_comp in self.graph[from_comp]:
                in_degree[to_comp] += 1
        
        queue = deque([comp for comp in self.components if in_degree[comp] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for neighbor in self.graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    def get_weight(self, from_comp: str, to_comp: str) -> float:
        return self.weights.get((from_comp, to_comp), 1.0)


class DependencyAnalyzer:
    
    def __init__(self, graph: DependencyGraph):
        self.graph = graph
        self.dfs_cache: Dict[str, Set[str]] = {}
    
    def find_dependencies_bfs(self, start: str) -> List[List[str]]:
        if start not in self.graph.components:
            return []
        
        visited = set()
        result = []
        queue = deque([(start, 0)])
        level_map = defaultdict(list)
        
        while queue:
            current, level = queue.popleft()
            
            if current in visited:
                continue
            
            visited.add(current)
            
            dependencies = self.graph.get_dependencies(current)
            
            for dep in dependencies:
                if dep not in visited:
                    level_map[level + 1].append(dep)
                    queue.append((dep, level + 1))
        
        if level_map:
            max_level = max(level_map.keys())
            for i in range(1, max_level + 1):
                if i in level_map:
                    unique_deps = []
                    seen = set()
                    for dep in level_map[i]:
                        if dep not in seen:
                            unique_deps.append(dep)
                            seen.add(dep)
                    result.append(unique_deps)
        
        return result
    
    def find_dependencies_dfs(self, start: str) -> Set[str]:
        if start not in self.graph.components:
            return set()
        
        if start in self.dfs_cache:
            return self.dfs_cache[start]
        
        visited = set()
        result = set()
        
        def dfs_recursive(component: str):
            if component in visited:
                return
            
            visited.add(component)
            dependencies = self.graph.get_dependencies(component)
            
            for dep in dependencies:
                result.add(dep)
                dfs_recursive(dep)
        
        dfs_recursive(start)
        
        self.dfs_cache[start] = result
        
        return result
    
    def clear_cache(self):
        self.dfs_cache.clear()
    
    def find_critical_path(self, start: str) -> Tuple[List[str], float]:
        if not self.graph.is_acyclic():
            raise ValueError("Граф содержит циклы. Критический путь можно найти только в ациклическом графе.")
        
        if start not in self.graph.components:
            return [], 0.0
        
        topo_order = self.graph.get_topological_order()
        if topo_order is None:
            return [], 0.0
        
        try:
            start_idx = topo_order.index(start)
        except ValueError:
            return [], 0.0
        
        dist = {comp: float('-inf') for comp in self.graph.components}
        dist[start] = 0.0
        parent = {comp: None for comp in self.graph.components}
        
        for i in range(start_idx, len(topo_order)):
            current = topo_order[i]
            if dist[current] == float('-inf'):
                continue
            
            for neighbor in self.graph.get_dependencies(current):
                weight = self.graph.get_weight(current, neighbor)
                new_dist = dist[current] + weight
                
                if new_dist > dist[neighbor]:
                    dist[neighbor] = new_dist
                    parent[neighbor] = current
        
        max_dist = float('-inf')
        max_vertex = None
        
        for comp, d in dist.items():
            if d > max_dist and d != float('-inf'):
                max_dist = d
                max_vertex = comp
        
        if max_vertex is None:
            return [], 0.0
        
        path = []
        current = max_vertex
        while current is not None:
            path.append(current)
            current = parent[current]
        
        path.reverse()
        
        return path, max_dist
    
    def visualize_graph(self, filename: str = "dependency_graph.png", 
                       highlight_component: Optional[str] = None):
        if not VISUALIZATION_AVAILABLE:
            raise ImportError(
                "Для визуализации необходимо установить networkx и matplotlib.\n"
                "Выполните: pip install networkx matplotlib"
            )
        
        G = nx.DiGraph()
        
        for from_comp in self.graph.graph:
            for to_comp in self.graph.graph[from_comp]:
                weight = self.graph.get_weight(from_comp, to_comp)
                G.add_edge(from_comp, to_comp, weight=weight)
        
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, 
                              connectionstyle='arc3,rad=0.1')
        
        node_colors = []
        for node in G.nodes():
            if highlight_component and node == highlight_component:
                node_colors.append('red')
            else:
                node_colors.append('lightblue')
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=2000, alpha=0.9)
        
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        edge_labels = {(u, v): f"{d['weight']:.1f}" 
                       for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
        
        plt.title("Граф зависимостей проекта", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Граф сохранён в файл: {filename}")
