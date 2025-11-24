from investment_optimizer import InvestmentOptimizer


def main():
    print("=" * 70)
    print("СИСТЕМА ОПТИМИЗАЦИИ ИНВЕСТИЦИОННОГО ПОРТФЕЛЯ")
    print("=" * 70)
    print()
    
    optimizer = InvestmentOptimizer()
    
    stocks = [(100, 10), (200, 30), (150, 20)]
    budget = 300
    bonds_yield = 5.0
    risk_limit = 0.5
    
    print("Исходные данные:")
    print(f"  Акции (стоимость, прибыль): {stocks}")
    print(f"  Бюджет: {budget}")
    print(f"  Доходность облигаций: {bonds_yield}%")
    print(f"  Лимит риска (макс. % в акции): {risk_limit * 100}%")
    print()
    
    print("1. ОДНОМЕРНОЕ ДП (Задача о рюкзаке)")
    print("-" * 70)
    profit_1d, selected_1d = optimizer.max_profit_1d(stocks, budget)
    print(f"Максимальная прибыль: {profit_1d}")
    print(f"Выбранные акции (индексы): {selected_1d}")
    print("Детали:")
    total_cost = 0
    for idx in selected_1d:
        cost, profit = stocks[idx]
        total_cost += cost
        print(f"  Акция {idx + 1}: стоимость {cost}, прибыль {profit}")
    print(f"Общая стоимость: {total_cost}, остаток бюджета: {budget - total_cost}")
    print()
    
    print("2. ДВУМЕРНОЕ ДП (Оптимизация риска и доходности)")
    print("-" * 70)
    profit_2d, stocks_amount, bonds_amount = optimizer.max_profit_2d(
        stocks, bonds_yield, budget, risk_limit
    )
    print(f"Максимальная прибыль: {profit_2d:.2f}")
    print(f"Инвестиции в акции: {stocks_amount}")
    print(f"Инвестиции в облигации: {bonds_amount}")
    print(f"Прибыль от акций: {profit_2d - bonds_amount * bonds_yield / 100.0:.2f}")
    print(f"Прибыль от облигаций: {bonds_amount * bonds_yield / 100.0:.2f}")
    print()
    
    print("3. СРАВНЕНИЕ С ЖАДНЫМ АЛГОРИТМОМ")
    print("-" * 70)
    profit_greedy, selected_greedy = optimizer.greedy_1d(stocks, budget)
    print(f"Динамическое программирование: прибыль {profit_1d}, акции {selected_1d}")
    print(f"Жадный алгоритм: прибыль {profit_greedy}, акции {selected_greedy}")
    print(f"Разница: {profit_1d - profit_greedy} ({((profit_1d - profit_greedy) / profit_1d * 100):.1f}%)")
    print()
    
    print("4. ТРЕХМЕРНОЕ ДП (С учетом временного горизонта)")
    print("-" * 70)
    time_horizon = 3
    total_investment, allocation = optimizer.max_profit_3d(
        stocks, bonds_yield, budget, risk_limit, time_horizon
    )
    print(f"Временной горизонт: {time_horizon} периодов")
    print("Распределение по периодам:")
    for period, (stocks_amt, bonds_amt) in allocation.items():
        stocks_profit = sum(profit for idx, (cost, profit) in enumerate(stocks) 
                           if stocks_amt >= cost)
        bonds_profit = bonds_amt * bonds_yield / 100.0 * period
        print(f"  Период {period}: акции {stocks_amt}, облигации {bonds_amt}, прибыль {stocks_profit + bonds_profit:.2f}")
    print()
    
    print("5. ВИЗУАЛИЗАЦИЯ")
    print("-" * 70)
    try:
        optimizer.visualize_profit_vs_budget(stocks, 500, step=20)
        print("График успешно создан!")
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")
        print("(Убедитесь, что установлен matplotlib)")
    print()
    
    print("=" * 70)
    print("АНАЛИЗ ЗАВЕРШЁН")
    print("=" * 70)


if __name__ == "__main__":
    main()

