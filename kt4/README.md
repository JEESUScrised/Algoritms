# Оптимизация инвестиционного портфеля

Система для формирования инвестиционного портфеля с использованием динамического программирования.

## Возможности

| Алгоритм | Описание | Сложность |
|----------|----------|-----------|
| Одномерное ДП | Максимизация прибыли от акций | O(n * B) |
| Двумерное ДП | Оптимизация распределения акции/облигации | O(n * B * R) |
| Трехмерное ДП | Учет временного горизонта | O(n * B * R * T) |
| Жадный алгоритм | Сравнение с оптимальным решением | O(n log n) |

## Использование

```python
from investment_optimizer import InvestmentOptimizer

optimizer = InvestmentOptimizer()
stocks = [(100, 10), (200, 30), (150, 20)]

profit, selected = optimizer.max_profit_1d(stocks, budget=300)
profit_2d, stocks_amt, bonds_amt = optimizer.max_profit_2d(
    stocks, bonds_yield=5.0, total_budget=300, risk_limit=0.5
)
```

## API

### InvestmentOptimizer

| Метод | Параметры | Возвращает |
|-------|-----------|------------|
| `max_profit_1d(stocks, budget)` | `stocks: List[Tuple[int, int]]`, `budget: int` | `Tuple[int, List[int]]` |
| `max_profit_2d(stocks, bonds_yield, total_budget, risk_limit)` | `stocks: List[Tuple[int, int]]`, `bonds_yield: float`, `total_budget: int`, `risk_limit: float` | `Tuple[float, int, int]` |
| `max_profit_3d(stocks, bonds_yield, total_budget, risk_limit, time_horizon)` | + `time_horizon: int` | `Tuple[float, Dict[int, Tuple[int, int]]]` |
| `greedy_1d(stocks, budget)` | `stocks: List[Tuple[int, int]]`, `budget: int` | `Tuple[int, List[int]]` |
| `visualize_profit_vs_budget(stocks, max_budget, step)` | `stocks: List[Tuple[int, int]]`, `max_budget: int`, `step: int` | `None` |

## Запуск

```bash
python example.py
```
