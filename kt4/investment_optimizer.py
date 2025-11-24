from typing import List, Tuple, Dict

try:
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    plt = None


class InvestmentOptimizer:
    
    def max_profit_1d(self, stocks: List[Tuple[int, int]], budget: int) -> Tuple[int, List[int]]:
        n = len(stocks)
        dp = [0] * (budget + 1)
        selected = [[] for _ in range(budget + 1)]
        
        for i in range(n):
            cost, profit = stocks[i]
            for j in range(budget, cost - 1, -1):
                if dp[j] < dp[j - cost] + profit:
                    dp[j] = dp[j - cost] + profit
                    selected[j] = selected[j - cost] + [i]
        
        max_profit = dp[budget]
        selected_stocks = selected[budget]
        
        return max_profit, selected_stocks
    
    def max_profit_2d(self, stocks: List[Tuple[int, int]], bonds_yield: float, 
                     total_budget: int, risk_limit: float) -> Tuple[float, int, int]:
        max_stocks_budget = int(total_budget * risk_limit)
        
        dp = [[0.0 for _ in range(max_stocks_budget + 1)] for _ in range(len(stocks) + 1)]
        stocks_amount = 0
        bonds_amount = 0
        max_profit = 0.0
        
        for i in range(1, len(stocks) + 1):
            cost, profit = stocks[i - 1]
            for j in range(max_stocks_budget + 1):
                dp[i][j] = dp[i - 1][j]
                
                if j >= cost:
                    new_profit = dp[i - 1][j - cost] + profit
                    if new_profit > dp[i][j]:
                        dp[i][j] = new_profit
        
        for j in range(max_stocks_budget + 1):
            stocks_investment = j
            bonds_investment = total_budget - stocks_investment
            stocks_profit = dp[len(stocks)][j]
            bonds_profit = bonds_investment * bonds_yield / 100.0
            total_profit = stocks_profit + bonds_profit
            
            if total_profit > max_profit:
                max_profit = total_profit
                stocks_amount = stocks_investment
                bonds_amount = bonds_investment
        
        return max_profit, stocks_amount, bonds_amount
    
    def max_profit_3d(self, stocks: List[Tuple[int, int]], bonds_yield: float,
                     total_budget: int, risk_limit: float, time_horizon: int) -> Tuple[float, Dict[int, Tuple[int, int]]]:
        max_stocks_budget = int(total_budget * risk_limit)
        
        dp = [[[0.0 for _ in range(max_stocks_budget + 1)] 
               for _ in range(len(stocks) + 1)] 
              for _ in range(time_horizon + 1)]
        
        allocation = {}
        
        for t in range(1, time_horizon + 1):
            for i in range(1, len(stocks) + 1):
                cost, profit = stocks[i - 1]
                for j in range(max_stocks_budget + 1):
                    dp[t][i][j] = dp[t][i - 1][j]
                    
                    if j >= cost:
                        new_profit = dp[t][i - 1][j - cost] + profit * t
                        if new_profit > dp[t][i][j]:
                            dp[t][i][j] = new_profit
        
        for t in range(1, time_horizon + 1):
            max_profit_t = 0.0
            best_stocks = 0
            best_bonds = 0
            
            for j in range(max_stocks_budget + 1):
                stocks_investment = j
                bonds_investment = total_budget - stocks_investment
                stocks_profit = dp[t][len(stocks)][j]
                bonds_profit = bonds_investment * bonds_yield / 100.0 * t
                total_profit = stocks_profit + bonds_profit
                
                if total_profit > max_profit_t:
                    max_profit_t = total_profit
                    best_stocks = stocks_investment
                    best_bonds = bonds_investment
            
            allocation[t] = (best_stocks, best_bonds)
        
        return allocation[time_horizon][0] + allocation[time_horizon][1], allocation
    
    def greedy_1d(self, stocks: List[Tuple[int, int]], budget: int) -> Tuple[int, List[int]]:
        ratios = [(i, profit / cost if cost > 0 else 0, cost, profit) 
                  for i, (cost, profit) in enumerate(stocks)]
        ratios.sort(key=lambda x: x[1], reverse=True)
        
        selected = []
        total_profit = 0
        remaining_budget = budget
        
        for i, _, cost, profit in ratios:
            if remaining_budget >= cost:
                selected.append(i)
                total_profit += profit
                remaining_budget -= cost
        
        return total_profit, selected
    
    def visualize_profit_vs_budget(self, stocks: List[Tuple[int, int]], 
                                   max_budget: int, step: int = 10):
        if not VISUALIZATION_AVAILABLE:
            raise ImportError(
                "Для визуализации необходимо установить matplotlib.\n"
                "Выполните: pip install matplotlib"
            )
        
        budgets = list(range(0, max_budget + 1, step))
        profits_dp = []
        profits_greedy = []
        
        for budget in budgets:
            profit_dp, _ = self.max_profit_1d(stocks, budget)
            profit_greedy, _ = self.greedy_1d(stocks, budget)
            profits_dp.append(profit_dp)
            profits_greedy.append(profit_greedy)
        
        plt.figure(figsize=(10, 6))
        plt.plot(budgets, profits_dp, marker='o', label='Динамическое программирование', linewidth=2)
        plt.plot(budgets, profits_greedy, marker='s', label='Жадный алгоритм', linewidth=2, linestyle='--')
        plt.xlabel('Бюджет')
        plt.ylabel('Прибыль')
        plt.title('Зависимость прибыли от бюджета')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('profit_vs_budget.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"График сохранён в файл: profit_vs_budget.png")

