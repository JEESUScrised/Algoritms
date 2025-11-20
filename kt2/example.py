from dependency_analyzer import DependencyGraph, DependencyAnalyzer


def load_dependencies_from_file(filename: str) -> DependencyGraph:
    graph = DependencyGraph()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if 'зависит от' in line:
                    parts = line.split('зависит от')
                    from_comp = parts[0].strip()
                    deps_str = parts[1].strip()
                elif '->' in line:
                    parts = line.split('->')
                    from_comp = parts[0].strip()
                    deps_str = parts[1].strip()
                else:
                    continue
                
                dependencies = [d.strip() for d in deps_str.split(',')]
                
                for dep in dependencies:
                    if dep:
                        graph.add_dependency(from_comp, dep)
    
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Используем пример из задания.")
    
    return graph


def main():
    print("=" * 60)
    print("СИСТЕМА АНАЛИЗА ЗАВИСИМОСТЕЙ В ПРОЕКТЕ")
    print("=" * 60)
    print()
    
    graph = DependencyGraph()
    
    print("1. Построение графа зависимостей:")
    print("   A зависит от B, C")
    print("   B зависит от D")
    print("   C зависит от D, E")
    print("   E зависит от B")
    print()
    
    graph.add_dependency("A", "B")
    graph.add_dependency("A", "C")
    graph.add_dependency("B", "D")
    graph.add_dependency("C", "D")
    graph.add_dependency("C", "E")
    graph.add_dependency("E", "B")
    
    print("2. Проверка на циклы (топологическая сортировка):")
    is_acyclic = graph.is_acyclic()
    print(f"   Граф ациклический: {is_acyclic}")
    
    if is_acyclic:
        topo_order = graph.get_topological_order()
        print(f"   Порядок сборки: {topo_order}")
        print("   Примечание: В данном графе нет прямого цикла.")
        print("   Путь C -> E -> B существует, но нет обратного пути от B к C.")
    else:
        print("   ОШИБКА: Обнаружен цикл! Проект нельзя собрать.")
    print()
    
    analyzer = DependencyAnalyzer(graph)
    
    print("3. Поиск зависимостей через BFS (по уровням) для компонента 'A':")
    bfs_result = analyzer.find_dependencies_bfs("A")
    print(f"   Результат: {bfs_result}")
    for i, level in enumerate(bfs_result, 1):
        print(f"   Уровень {i}: {level}")
    print()
    
    print("4. Поиск зависимостей через DFS для компонента 'A':")
    dfs_result = analyzer.find_dependencies_dfs("A")
    print(f"   Результат: {sorted(dfs_result)}")
    print()
    
    print("5. Пример графа С циклом:")
    graph_cycle = DependencyGraph()
    graph_cycle.add_dependency("A", "B")
    graph_cycle.add_dependency("B", "C")
    graph_cycle.add_dependency("C", "A")
    
    print("   A зависит от B")
    print("   B зависит от C")
    print("   C зависит от A (ЦИКЛ!)")
    print()
    
    is_acyclic_cycle = graph_cycle.is_acyclic()
    print(f"   Граф ациклический: {is_acyclic_cycle}")
    
    if is_acyclic_cycle:
        topo_order_cycle = graph_cycle.get_topological_order()
        print(f"   Порядок сборки: {topo_order_cycle}")
    else:
        print("   ОШИБКА: Обнаружен цикл! Проект нельзя собрать.")
    print()
    
    print("6. Пример графа БЕЗ циклов:")
    graph2 = DependencyGraph()
    graph2.add_dependency("A", "B")
    graph2.add_dependency("A", "C")
    graph2.add_dependency("B", "D")
    graph2.add_dependency("C", "D")
    graph2.add_dependency("C", "E")
    
    print("   A зависит от B, C")
    print("   B зависит от D")
    print("   C зависит от D, E")
    print()
    
    is_acyclic2 = graph2.is_acyclic()
    print(f"   Граф ациклический: {is_acyclic2}")
    
    if is_acyclic2:
        topo_order2 = graph2.get_topological_order()
        print(f"   Порядок сборки: {topo_order2}")
    print()
    
    analyzer2 = DependencyAnalyzer(graph2)
    
    print("   BFS для 'A':")
    bfs_result2 = analyzer2.find_dependencies_bfs("A")
    print(f"   {bfs_result2}")
    
    print("   DFS для 'A':")
    dfs_result2 = analyzer2.find_dependencies_dfs("A")
    print(f"   {sorted(dfs_result2)}")
    print()
    
    print("7. Пример с весами рёбер и критическим путём:")
    graph3 = DependencyGraph()
    graph3.add_dependency("A", "B", weight=2.0)
    graph3.add_dependency("A", "C", weight=3.0)
    graph3.add_dependency("B", "D", weight=1.0)
    graph3.add_dependency("C", "D", weight=4.0)
    graph3.add_dependency("C", "E", weight=2.0)
    
    analyzer3 = DependencyAnalyzer(graph3)
    
    try:
        path, total_weight = analyzer3.find_critical_path("A")
        print(f"   Критический путь от 'A': {path}")
        print(f"   Общий вес: {total_weight}")
    except ValueError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("8. Визуализация графа:")
    try:
        analyzer2.visualize_graph("dependency_graph.png", highlight_component="A")
        print("   Граф успешно визуализирован!")
    except Exception as e:
        print(f"   Ошибка при визуализации: {e}")
        print("   (Убедитесь, что установлены networkx и matplotlib)")
    print()
    
    print("9. Демонстрация кэширования DFS:")
    print("   Первый вызов DFS для 'A' (без кэша)...")
    result1 = analyzer2.find_dependencies_dfs("A")
    print(f"   Результат: {sorted(result1)}")
    print("   Второй вызов DFS для 'A' (из кэша)...")
    result2 = analyzer2.find_dependencies_dfs("A")
    print(f"   Результат: {sorted(result2)}")
    print(f"   Результаты совпадают: {result1 == result2}")
    print()
    
    print("=" * 60)
    print("АНАЛИЗ ЗАВЕРШЁН")
    print("=" * 60)


if __name__ == "__main__":
    main()
