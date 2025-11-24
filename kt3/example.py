from transport_network import TransportGraph, NetworkOptimizer


def create_example_network():
    graph = TransportGraph()
    routes = [
        ("A", "B", 4), ("B", "A", 4),
        ("A", "C", 2), ("C", "A", 2),
        ("B", "C", 1), ("C", "B", 1),
        ("B", "D", 5), ("D", "B", 5),
        ("C", "D", 8), ("D", "C", 8)
    ]
    for from_station, to_station, weight in routes:
        graph.add_route(from_station, to_station, weight)
    return graph


def create_city_network():
    graph = TransportGraph()
    routes = [
        ("Центр. вокзал", "Пл. Ленина", 1.2), ("Пл. Ленина", "Центр. вокзал", 1.2),
        ("Центр. вокзал", "Автостанция-1", 3.5), ("Автостанция-1", "Центр. вокзал", 3.5),
        ("Центр. вокзал", "Вокзал-Северный", 4.0), ("Вокзал-Северный", "Центр. вокзал", 4.0),
        ("Пл. Ленина", "Автостанция-1", 2.1), ("Автостанция-1", "Пл. Ленина", 2.1),
        ("Пл. Ленина", "Университет", 0.8), ("Университет", "Пл. Ленина", 0.8),
        ("Пл. Ленина", "Автостанция-2", 3.0), ("Автостанция-2", "Пл. Ленина", 3.0),
        ("Пл. Ленина", "Парковая", 1.5), ("Парковая", "Пл. Ленина", 1.5),
        ("Автостанция-1", "Автостанция-2", 5.4), ("Автостанция-2", "Автостанция-1", 5.4),
        ("Автостанция-1", "Портовая", 4.2), ("Портовая", "Автостанция-1", 4.2),
        ("Университет", "Вокзал-Северный", 2.7), ("Вокзал-Северный", "Университет", 2.7),
        ("Университет", "Автостанция-2", 1.9), ("Автостанция-2", "Университет", 1.9),
        ("Вокзал-Северный", "Парковая", 3.3), ("Парковая", "Вокзал-Северный", 3.3),
        ("Вокзал-Северный", "Портовая", 6.0), ("Портовая", "Вокзал-Северный", 6.0),
        ("Автостанция-2", "Парковая", 2.5), ("Парковая", "Автостанция-2", 2.5)
    ]
    for from_station, to_station, weight in routes:
        graph.add_route(from_station, to_station, weight)
    return graph


def print_distances(title, distances):
    print(f"{title}:")
    for station, distance in sorted(distances.items()):
        if distance == float('inf'):
            print(f"  {station}: недостижима")
        else:
            print(f"  {station}: {distance:.1f}" if isinstance(distance, float) and distance % 1 != 0 else f"  {station}: {int(distance)}")
    print()


def print_mst(title, edges, weight):
    print(f"{title}:")
    for from_station, to_station, weight_edge in edges:
        print(f"  {from_station} <-> {to_station}: {weight_edge:.1f}" if weight_edge % 1 != 0 else f"  {from_station} <-> {to_station}: {int(weight_edge)}")
    print(f"  Суммарный вес: {weight:.1f}" if weight % 1 != 0 else f"  Суммарный вес: {int(weight)}")
    print()


def print_matrix(title, matrix, stations):
    print(f"{title}:")
    print("     ", end="")
    for station in stations:
        print(f"{station[:12]:>12}", end="")
    print()
    for i, station in enumerate(stations):
        print(f"{station[:12]:>12}", end="")
        for j in range(len(stations)):
            dist = matrix[i][j]
            if dist == float('inf'):
                print(f"{'inf':>12}", end="")
            else:
                print(f"{dist:>12.1f}", end="")
        print()
    print()


def main():
    print("=" * 70)
    print("СИСТЕМА ОПТИМИЗАЦИИ ГОРОДСКОЙ ТРАНСПОРТНОЙ СЕТИ")
    print("=" * 70)
    print()
    
    print("1. ПРИМЕР ИЗ ЗАДАНИЯ")
    print("-" * 70)
    graph = create_example_network()
    
    print_distances("Кратчайшие пути от 'A' (Дейкстра)", graph.shortest_path_Dijkstra("A"))
    
    bf_result, has_cycle = graph.shortest_path_BellmanFord("A")
    if has_cycle:
        print("Кратчайшие пути от 'A' (Беллман-Форд): Обнаружен отрицательный цикл!\n")
    else:
        print_distances("Кратчайшие пути от 'A' (Беллман-Форд)", bf_result)
    
    optimizer = NetworkOptimizer(graph)
    mst_kruskal, total_kruskal = optimizer.minimum_spanning_tree_Kruskal()
    print_mst("Минимальное остовное дерево (Крускал)", mst_kruskal, total_kruskal)
    
    mst_prim, total_prim = optimizer.minimum_spanning_tree_Prim("A")
    print_mst("Минимальное остовное дерево (Прим)", mst_prim, total_prim)
    
    floyd_matrix = graph.all_pairs_shortest_paths_FloydWarshall()
    print_matrix("Матрица кратчайших расстояний (Флойд-Уоршелл)", floyd_matrix, graph.get_all_stations())
    
    print("=" * 70)
    print("2. ГОРОДСКАЯ ТРАНСПОРТНАЯ СЕТЬ (8 УЗЛОВ)")
    print("=" * 70)
    print()
    
    city_graph = create_city_network()
    
    print_distances("Кратчайшие пути от 'Центр. вокзал' (Дейкстра)", 
                   city_graph.shortest_path_Dijkstra("Центр. вокзал"))
    
    city_bf, has_negative_cycle = city_graph.shortest_path_BellmanFord("Центр. вокзал")
    if has_negative_cycle:
        print("Проверка на отрицательные циклы: Обнаружен отрицательный цикл!\n")
    else:
        print("Проверка на отрицательные циклы: Отрицательных циклов не обнаружено.\n")
    
    city_optimizer = NetworkOptimizer(city_graph)
    city_mst_kruskal, city_total_kruskal = city_optimizer.minimum_spanning_tree_Kruskal()
    print_mst("Минимальная транспортная сеть (Крускал)", city_mst_kruskal, city_total_kruskal)
    
    city_mst_prim, city_total_prim = city_optimizer.minimum_spanning_tree_Prim("Центр. вокзал")
    print_mst("Минимальная транспортная сеть (Прим)", city_mst_prim, city_total_prim)
    
    city_floyd = city_graph.all_pairs_shortest_paths_FloydWarshall()
    print_matrix("Матрица кратчайших расстояний между всеми станциями", 
                city_floyd, city_graph.get_all_stations())
    
    print("=" * 70)
    print("АНАЛИЗ ЗАВЕРШЁН")
    print("=" * 70)


if __name__ == "__main__":
    main()
