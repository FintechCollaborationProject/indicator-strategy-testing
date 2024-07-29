import pandas as pd
import numpy as np

class BacktestMetrics:
    def __init__(self, history, initial_balance):
        self.history = history
        self.initial_balance = initial_balance

        # Check if 'Profit' column exists
        if 'Profit' not in self.history.columns:
            print("Error: 'Profit' column not found in history.")
        else:
            # Calculate the Portfolio Value at each point
            self.history['Portfolio Value'] = self.initial_balance + self.history['Profit'].cumsum()

    def total_return(self):
        if self.history.empty or 'Portfolio Value' not in self.history.columns:
            print("Warning: History is empty or 'Portfolio Value' column missing. Returning 0 for total return.")
            return 0  
        final_balance = self.history['Portfolio Value'].iloc[-1]
        total_return = (final_balance - self.initial_balance) / self.initial_balance * 100
        return total_return

    def annualized_return(self):
        if self.history is None or self.history.empty:
            return 0.0
        self.history['Date'] = pd.to_datetime(self.history['Date'])
        self.history.set_index('Date', inplace=True)
        num_days = (self.history.index[-1] - self.history.index[0]).days
        total_return = self.history['Portfolio Value'].iloc[-1] / self.history['Portfolio Value'].iloc[0] - 1
        annualized_return = (1 + total_return) ** (365.0 / num_days) - 1 if num_days > 0 else 0
        return annualized_return * 100

    def sharpe_ratio(self, risk_free_rate=0.01):
        if 'Profit' not in self.history.columns or self.history.empty:
            return 0.0
        returns = self.history['Profit'] / self.initial_balance
        excess_returns = returns - risk_free_rate / len(self.history)
        if excess_returns.std() == 0:
            return 0.0
        sharpe_ratio = np.sqrt(len(returns)) * excess_returns.mean() / excess_returns.std()
        return sharpe_ratio

    def max_drawdown(self):
        if self.history.empty or 'Profit' not in self.history.columns:
            return 0.0
        balance = self.history['Profit'].cumsum() + self.initial_balance
        drawdown = (balance.cummax() - balance) / balance.cummax()
        max_drawdown = drawdown.max() * 100
        return max_drawdown

    def calculate_all_metrics(self):
        metrics = {
            'Total Return (%)': self.total_return(),
            'Annualized Return (%)': self.annualized_return(),
            'Sharpe Ratio': self.sharpe_ratio(),
            'Max Drawdown (%)': self.max_drawdown()
        }
        return metrics

    def calculate_annual_returns(self):
        if 'Date' not in self.history.columns:
            print("Error: 'Date' column not found in history. Columns present:", self.history.columns)
            return []
        self.history['Date'] = pd.to_datetime(self.history['Date'])
        self.history.set_index('Date', inplace=True)
        self.history['Cumulative Balance'] = self.history['Profit'].cumsum() + self.initial_balance
        annual_returns = []
        for year, group in self.history.groupby(self.history.index.year):
            start_value = group['Cumulative Balance'].iloc[0]
            end_value = group['Cumulative Balance'].iloc[-1]
            annual_return = (end_value - start_value) / start_value * 100
            annual_returns.append(annual_return)
        return annual_returns
