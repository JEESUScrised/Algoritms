# словарь из задания
EXAMPLE_WORD_FREQUENCIES = {
    "apple": 10,
    "application": 5,
    "banana": 3,
    "book": 8,
    "binary": 1,
    "bee": 7,
    "bat": 4,
    "ball": 2
}

# большой словарь
EXTENDED_WORD_FREQUENCIES = {
    "apple": 10, "application": 5, "banana": 3, "book": 8, "binary": 1,
    "bee": 7, "bat": 4, "ball": 2, "cat": 6, "car": 9, "computer": 4,
    "code": 8, "data": 7, "database": 3, "design": 5, "development": 6,
    "algorithm": 9, "analysis": 4, "array": 8, "binary_tree": 2, "cache": 5,
    "python": 12, "programming": 7, "javascript": 6, "java": 8, "csharp": 3,
    "react": 9, "angular": 4, "vue": 5, "nodejs": 6, "express": 4,
    "database": 3, "sql": 8, "mongodb": 5, "redis": 4, "postgresql": 3,
    "docker": 7, "kubernetes": 4, "aws": 9, "azure": 5, "gcp": 3,
    "machine": 6, "learning": 8, "artificial": 5, "intelligence": 7,
    "neural": 4, "network": 6, "deep": 5, "data": 7, "science": 6
}

# Тестовые запросы
TEST_QUERIES = [
    ("app", 1),  # VIP запрос
    ("b", 0),    # обычный запрос
    ("ba", 1),   
    ("be", 0),   
    ("pro", 1),  
    ("da", 0),   # ожидание: ["data", "database"]
    ("al", 1),   
    ("ja", 0),   
]

def run_basic_example():
    """Запуск базового примера из задания"""
    from search_system import SearchSystem
    
    print("=== Базовый пример из задания ===")
    system = SearchSystem()
    system.load_words_from_dict(EXAMPLE_WORD_FREQUENCIES)
    
    # тест автодополнения
    print("\nТестирование автодополнения:")
    test_cases = [
        ("app", ["apple", "application"]),
        ("b", ["book", "bee", "bat", "banana", "ball"])
    ]
    
    for prefix, expected in test_cases:
        result = system.trie.autocomplete(prefix)
        print(f"Префикс '{prefix}': {result}")
        print(f"Ожидалось: {expected}")
        print(f"Совпадает: {result == expected}")
        print()

if __name__ == "__main__":
    run_basic_example()
