import heapq
import time
# from typing import List, Tuple, Optional  # закомментировал, не всегда работает
from collections import defaultdict


class TrieNode:
    # узел древа для хранения слов
    
    def __init__(self):
        self.children = {}  # дети узла
        self.is_end = False  # конец слова или нет
        self.frequency = 0  # сколько раз встречается


class Trie:
    # префиксное дерево
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, frequency=1):
        # добавляем слово в дерево
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += frequency
    
    def search(self, word):
        # ищем слово в дереве
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def _get_all_words_with_prefix(self, prefix):
        # получаем все слова с префиксом
        node = self.root
        # идем по префиксу
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # собираем слова
        words = []
        self._dfs_collect_words(node, prefix, words)
        return words
    
    def _dfs_collect_words(self, node, current_word, words):
        if node.is_end:
            words.append((current_word, node.frequency))
        
        for char, child_node in node.children.items():
            self._dfs_collect_words(child_node, current_word + char, words)
    
    def autocomplete(self, prefix, top_k=5):
        # возвращаем топ слов
        words_with_freq = self._get_all_words_with_prefix(prefix)
        
        if not words_with_freq:
            return []
        
        # чуча сорт по честоте
        # max-heap через отрицательные числа
        max_heap = []
        for word, freq in words_with_freq:
            heapq.heappush(max_heap, (-freq, word)) 
        #  топ-k
        result = []
        for i in range(min(top_k, len(max_heap))):
            if max_heap:
                neg_freq, word = heapq.heappop(max_heap)
                result.append(word)

        return result
    
    def remove(self, word):
        # удаляем слово из дерева
        if not self.search(word):
            return False
        
        # находим путь к слову
        path = [self.root]
        node = self.root
        for char in word:
            node = node.children[char]
            path.append(node)
        
        # убираем флаг конца слова
        path[-1].is_end = False
        path[-1].frequency = 0
        
        # удаляем пустые узлы
        for i in range(len(path) - 1, 0, -1):
            current_node = path[i]
            parent_node = path[i - 1]
            char = word[i - 1]
            
            if not current_node.children and not current_node.is_end:
                del parent_node.children[char]
            else:
                break
        
        return True


class PriorityQueue:
    # очередь с приоритетами
    
    def __init__(self):
        self.heap = []  # куча для приоритетов
        self.counter = 0  
    
    def enqueue(self, request, priority=0):
        # добавляем запрос в очередь
        # приоритет 1 = VIP, 0 = обычный
        if priority == 1:  
            priority = -1
        heapq.heappush(self.heap, (priority, self.counter, request))
        self.counter += 1
    
    def dequeue(self):
        # берем запрос приоритетом
        if not self.heap:
            return None
        
        priority, counter, request = heapq.heappop(self.heap)
        return request
    
    def is_empty(self):
        # проверяем пуста ли очередь
        return len(self.heap) == 0
    
    def size(self):
        # размер очереди
        return len(self.heap)


class SearchSystem:
    # основная система поиска
    
    def __init__(self):
        self.trie = Trie()
        self.priority_queue = PriorityQueue()
        self.request_count = 0
        self.processed_count = 0
    
    def load_words_from_dict(self, word_frequencies):
        # загружаем словарь
        for word, frequency in word_frequencies.items():
            self.trie.insert(word, frequency)
        print(f"Загружено {len(word_frequencies)} слов в словарь")
    
    def add_request(self, prefix, priority=0):
        # добавляем запрос
        self.priority_queue.enqueue(prefix, priority)
        self.request_count += 1
    
    def process_requests(self):
        # обрабатываем запросы
        results = []
        
        while not self.priority_queue.is_empty():
            prefix = self.priority_queue.dequeue()
            if prefix:
                suggestions = self.trie.autocomplete(prefix)
                results.append((prefix, suggestions))
                self.processed_count += 1
                print(f"Обработан запрос '{prefix}': {suggestions}")
        
        return results
    
    def get_statistics(self):
        # статы
        return {
            'total_requests': self.request_count,
            'processed_requests': self.processed_count,
            'queue_size': self.priority_queue.size()
        }


def performance_test(num_requests=10000):
    # производительность
    print(f"\n=== Тестирование производительности ({num_requests} запросов) ===")
    
    # создаем систему
    system = SearchSystem()
    
    # тестовые слова
    test_words = {
        "apple": 10, "application": 5, "banana": 3, "book": 8, "binary": 1,
        "bee": 7, "bat": 4, "ball": 2, "cat": 6, "car": 9, "computer": 4,
        "code": 8, "data": 7, "database": 3, "design": 5, "development": 6,
        "algorithm": 9, "analysis": 4, "array": 8, "binary_tree": 2, "cache": 5
    }
    system.load_words_from_dict(test_words)
    
    # генерируем запросы
    prefixes = ["a", "b", "c", "d", "app", "ba", "co", "al", "bi", "ca"]
    priorities = [0, 1] 
    
    start_time = time.time()
    
    # добавляем запросы
    for i in range(num_requests):
        prefix = prefixes[i % len(prefixes)]
        priority = priorities[i % len(priorities)]
        system.add_request(prefix, priority)
    

    results = system.process_requests()
    
    end_time = time.time()
    
    # статистика
    stats = system.get_statistics()
    stats['execution_time'] = end_time - start_time
    stats['requests_per_second'] = num_requests / stats['execution_time']
    
    print(f"Время выполнения: {stats['execution_time']:.4f} секунд")
    print(f"Запросов в секунду: {stats['requests_per_second']:.2f}")
    print(f"Обработано запросов: {stats['processed_requests']}")
    
    return stats


def main():
    
    print("=== Система обработки поисковых запросов ===\n")
    
    # создаем систему
    system = SearchSystem()
    
    # словарь из задания
    word_frequencies = {
        "apple": 10, "application": 5, "banana": 3, "book": 8, "binary": 1,
        "bee": 7, "bat": 4, "ball": 2
    }
    system.load_words_from_dict(word_frequencies)
    
    print("\n=== Тестирование автодополнения ===")
    test_prefixes = ["app", "b", "ba", "be", "bo"]
    for prefix in test_prefixes:
        suggestions = system.trie.autocomplete(prefix)
        print(f"Префикс '{prefix}': {suggestions}")
    
    print("\n=== Обработка запросов с приоритетами ===")
    
    # добавляем запросы
    system.add_request("app", priority=1)  # VIP
    system.add_request("b", priority=0)    # обычный
    system.add_request("ba", priority=1)   
    system.add_request("be", priority=0)   
    
    print("Добавлены запросы в очередь")
    print("Обработка (VIP запросы первыми):")
    
 
    results = system.process_requests()
    
    print(f"\nСтатистика: {system.get_statistics()}")
    
    print("\n=== Тестирование удаления слов ===")
    print("Удаляем слово 'apple'...")
    if system.trie.remove("apple"):
        print("Слово удалено")
        print(f"Автодополнение для 'app': {system.trie.autocomplete('app')}")
    else:
        print("Слово не найдено")
    

    performance_test(1000)


if __name__ == "__main__":
    main()
