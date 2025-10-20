from search_system import SearchSystem

def main():
    print("=== ПРОСТОЙ ПРИМЕР РАБОТЫ СИСТЕМЫ ===\n")
    
    # создаем систему
    system = SearchSystem()
    
    # словарь из задания
    word_frequencies = {
        "apple": 10, "application": 5, "banana": 3, "book": 8, "binary": 1,
        "bee": 7, "bat": 4, "ball": 2
    }
    system.load_words_from_dict(word_frequencies)
    
    print("1. Тестирование автодополнения:")
    print(f"   'app' → {system.trie.autocomplete('app')}")
    print(f"   'b' → {system.trie.autocomplete('b')}")
    print(f"   'ba' → {system.trie.autocomplete('ba')}")
    
    print("\n2. Добавление запросов с приоритетами:")
    print("   VIP запрос (приоритет 1): 'app'")
    print("   Обычный запрос (приоритет 0): 'b'")
    print("   VIP запрос (приоритет 1): 'ba'")
    print("   Обычный запрос (приоритет 0): 'be'")
    
    # добавляем запросы
    system.add_request("app", priority=1)  # VIP
    system.add_request("b", priority=0)    # обычный
    system.add_request("ba", priority=1)   
    system.add_request("be", priority=0)   
    
    print(f"\n   Размер очереди: {system.priority_queue.size()}")
    
    print("\n3. Обработка запросов (VIP запросы обрабатываются первыми):")
    results = system.process_requests()
    
    print(f"\n4. Статистика:")
    stats = system.get_statistics()
    print(f"   Всего запросов: {stats['total_requests']}")
    print(f"   Обработано: {stats['processed_requests']}")
    
    print("\n5. Тестирование удаления слова:")
    print("   Удаляем 'apple'...")
    if system.trie.remove("apple"):
        print("   Слово удалено успешно")
        print(f"   Автодополнение 'app': {system.trie.autocomplete('app')}")
    else:
        print("   Слово не найдено")

if __name__ == "__main__":
    main()
