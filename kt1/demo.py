from search_system import SearchSystem, performance_test
from test_data import EXAMPLE_WORD_FREQUENCIES, EXTENDED_WORD_FREQUENCIES, TEST_QUERIES
 # я устал писать комменты :)
def demo_basic_functionality():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ СИСТЕМЫ ПОИСКОВЫХ ЗАПРОСОВ")
    print("=" * 60)
    
    system = SearchSystem()


    print("\n1. Загрузка словаря...")
    system.load_words_from_dict(EXAMPLE_WORD_FREQUENCIES)
    
  
    print("\n2. Тестирование поиска слов:")
    test_words = ["apple", "banana", "nonexistent"]
    for word in test_words:
        found = system.trie.search(word)
        print(f"   Слово '{word}': {'найдено' if found else 'не найдено'}")
    
  
    print("\n3. Тестирование автодополнения:")
    prefixes = ["app", "b", "ba", "be", "bo"]
    for prefix in prefixes:
        suggestions = system.trie.autocomplete(prefix, top_k=3)
        print(f"   Префикс '{prefix}': {suggestions}")

def demo_priority_queue():
    """Демонстрация работы приоритетов"""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ОЧЕРЕДИ ПРИОРИТЕТОВ")
    print("=" * 60)
    
    system = SearchSystem()
    system.load_words_from_dict(EXAMPLE_WORD_FREQUENCIES)
    
    print("\nДобавление запросов в очередь:")
    queries = [
        ("app", 0, "Обычный запрос"),
        ("b", 1, "VIP запрос"),
        ("ba", 0, "Обычный запрос"),
        ("be", 1, "VIP запрос")
    ]
    
    for prefix, priority, description in queries:
        system.add_request(prefix, priority)
        print(f"   {description}: '{prefix}' (приоритет {priority})")
    
    print(f"\nРазмер очереди: {system.priority_queue.size()}")
    
    print("\nОбработка запросов (VIP запросы обрабатываются первыми):")
    results = system.process_requests()
    
    print(f"\nОбработано запросов: {len(results)}")

def demo_word_removal():
    """Демонстрация удаления слов"""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ УДАЛЕНИЯ СЛОВ")
    print("=" * 60)
    
    system = SearchSystem()
    system.load_words_from_dict(EXAMPLE_WORD_FREQUENCIES)
    
    print("\nАвтодополнение до удаления:")
    print(f"   'app': {system.trie.autocomplete('app')}")
    
    print("\nУдаляем слово 'apple'...")
    if system.trie.remove("apple"):
        print("   Слово успешно удалено")
    else:
        print("   Слово не найдено")
    
    print("\nАвтодополнение после удаления:")
    print(f"   'app': {system.trie.autocomplete('app')}")
    
    print(f"\nПоиск слова 'apple': {'найдено' if system.trie.search('apple') else 'не найдено'}")

def demo_performance():
    """Демонстрация тестирования производительности"""
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
  
    test_sizes = [100, 1000, 5000]
    
    for size in test_sizes:
        print(f"\nТестирование с {size} запросами:")
        stats = performance_test(size)
        print(f"   Время выполнения: {stats['execution_time']:.4f} сек")
        print(f"   Запросов в секунду: {stats['requests_per_second']:.2f}")

def demo_extended_features():
    """Демонстрация расширенных возможностей"""
    print("\n" + "=" * 60)
    print("РАСШИРЕННЫЕ ВОЗМОЖНОСТИ")
    print("=" * 60)
    
    system = SearchSystem()
    system.load_words_from_dict(EXTENDED_WORD_FREQUENCIES)
    
    print("\nТестирование с расширенным словарем:")
    test_prefixes = ["pro", "da", "al", "ja", "ma"]
    
    for prefix in test_prefixes:
        suggestions = system.trie.autocomplete(prefix, top_k=5)
        print(f"   '{prefix}': {suggestions}")
    

    print("\nОбработка множественных запросов:")
    for prefix, priority in TEST_QUERIES[:6]: 
        system.add_request(prefix, priority)
    
    print(f"Добавлено {len(TEST_QUERIES[:6])} запросов в очередь")
    results = system.process_requests()
    print(f"Обработано {len(results)} запросов")

def main():
    """Главная функция демонстрации"""
    try:
        demo_basic_functionality()
        demo_priority_queue()
        demo_word_removal()
        demo_performance()
        demo_extended_features()
        
        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
