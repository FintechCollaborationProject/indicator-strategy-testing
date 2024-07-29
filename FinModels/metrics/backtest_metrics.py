import pandas as pd
import numpy as np

class BacktestMetrics:
    def __init__(self, history, initial_balance):
        """
        Initialize BacktestMetrics with trade history and initial balance.

        :param history: DataFrame containing trade history with 'Date' and 'Profit' columns.
        :param initial_balance: Initial balance at the start of the backtest.
        """
        self.history = history.copy()
        self.initial_balance = initial_balance

        if 'Profit' not in self.history.columns:
            raise ValueError("Error: 'Profit' column not found in history.")
        
        # Calculate the Portfolio Value at each point
        self.history['Portfolio Value'] = self.initial_balance + self.history['Profit'].cumsum()

    def total_return(self):
        """
        Calculate the total return of the backtest.

        :return: Total return as a percentage.
        """
        if self.history.empty or 'Portfolio Value' not in self.history.columns:
            return 0.0
        final_balance = self.history['Portfolio Value'].iloc[-1]
        total_return = (final_balance - self.initial_balance) / self.initial_balance * 100
        return total_return

    def annualized_return(self):
        """
        Calculate the annualized return of the backtest.

        :return: Annualized return as a percentage.
        """
        if self.history.empty:
            return 0.0

        self.history['Date'] = pd.to_datetime(self.history['Date'])
        num_days = (self.history['Date'].iloc[-1] - self.history['Date'].iloc[0]).days

        if num_days <= 0:
            return 0.0

        total_return = self.history['Portfolio Value'].iloc[-1] / self.initial_balance - 1
        annualized_return = (1 + total_return) ** (365.0 / num_days) - 1
        return annualized_return * 100

    def sharpe_ratio(self, risk_free_rate=0.01):
        """
        Calculate the Sharpe Ratio of the backtest.

        :param risk_free_rate: Risk-free rate used for Sharpe Ratio calculation (annualized).
        :return: Sharpe Ratio.
        """
        if self.history.empty or 'Profit' not in self.history.columns:
            return 0.0

        returns = self.history['Profit'] / self.initial_balance
        excess_returns = returns - risk_free_rate / 365  # Assuming daily returns

        if excess_returns.std() == 0:
            return 0.0

        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()  # Assuming 252 trading days in a year
        return sharpe_ratio

    def max_drawdown(self):
        """
        Calculate the maximum drawdown of the backtest.

        :return: Max drawdown as a percentage.
        """
        if self.history.empty or 'Portfolio Value' not in self.history.columns:
            return 0.0

        rolling_max = self.history['Portfolio Value'].cummax()
        drawdown = (rolling_max - self.history['Portfolio Value']) / rolling_max
        max_drawdown = drawdown.max() * 100
        return max_drawdown

    def calculate_all_metrics(self):
        """
        Calculate and return all metrics.

        :return: Dictionary of all calculated metrics.
        """
        metrics = {
            'Total Return (%)': self.total_return(),
            'Annualized Return (%)': self.annualized_return(),
            'Sharpe Ratio': self.sharpe_ratio(),
            'Max Drawdown (%)': self.max_drawdown()
        }
        return metrics

    def calculate_annual_returns(self):
        """
        Calculate annual returns based on the portfolio value.

        :return: List of annual returns as percentages.
        """
        if 'Date' not in self.history.columns:
            print("Error: 'Date' column not found in history.")
            return []

        self.history['Date'] = pd.to_datetime(self.history['Date'])
        self.history.set_index('Date', inplace=True)
        self.history['Cumulative Balance'] = self.history['Profit'].cumsum() + self.initial_balance
        annual_returns = []

        for year, group in self.history.groupby(self.history.index.year):
            if not group.empty:
                start_value = group['Cumulative Balance'].iloc[0]
                end_value = group['Cumulative Balance'].iloc[-1]
                annual_return = (end_value - start_value) / start_value * 100
                annual_returns.append(annual_return)

        return annual_returns
