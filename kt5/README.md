# Оптимизация городской транспортной сети

## Возможности

| Алгоритм | Описание | Сложность |
|----------|----------|-----------|
| Дейкстра | Кратчайшие пути от одной вершины | O((V + E) log V) |
| Беллман-Форд | Кратчайшие пути с проверкой отрицательных циклов | O(V * E) |
| Флойд-Уоршелл | Матрица расстояний между всеми парами | O(V³) |
| Крускал | Минимальное остовное дерево | O(E log E) |
| Прим | Минимальное остовное дерево (жадный) | O((V + E) log V) |

## Использование

```python
from transport_network import TransportGraph, NetworkOptimizer

graph = TransportGraph()
graph.add_route("A", "B", 4)
graph.add_route("A", "C", 2)

dijkstra = graph.shortest_path_Dijkstra("A")
optimizer = NetworkOptimizer(graph)
mst_edges, total_weight = optimizer.minimum_spanning_tree_Kruskal()
```

## API

### TransportGraph

| Метод | Параметры | Возвращает |
|-------|-----------|------------|
| `add_station(name)` | `name: str` | `None` |
| `add_route(from, to, weight)` | `from: str`, `to: str`, `weight: float` | `None` |
| `shortest_path_Dijkstra(start)` | `start: str` | `Dict[str, float]` |
| `shortest_path_BellmanFord(start)` | `start: str` | `Tuple[Dict[str, float], bool]` |
| `all_pairs_shortest_paths_FloydWarshall()` | - | `List[List[float]]` |

### NetworkOptimizer

| Метод | Параметры | Возвращает |
|-------|-----------|------------|
| `minimum_spanning_tree_Kruskal()` | - | `Tuple[List[Tuple[str, str, float]], float]` |
| `minimum_spanning_tree_Prim(start)` | `start: str \| None` | `Tuple[List[Tuple[str, str, float]], float]` |

## Запуск

```bash
python example.py
```
