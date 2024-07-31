import pandas as pd
import numpy as np

class BacktestMetrics:
    def __init__(self, history, initial_balance, start_date, end_date):
        """
        Initialize BacktestMetrics with trade history, initial balance, and fixed date range.

        :param history: DataFrame containing trade history with 'Date' and 'Profit' columns.
        :param initial_balance: Initial balance at the start of the backtest.
        :param start_date: The start date of the trading period (inclusive).
        :param end_date: The end date of the trading period (inclusive).
        """
        self.history = history.copy()
        self.initial_balance = initial_balance
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)

        assert 'Profit' in self.history.columns, "Error: 'Profit' column not found in history."

        self.history['Portfolio Value'] = self.initial_balance + self.history['Profit'].cumsum()
        self.history['Date'] = pd.to_datetime(self.history['Date'])

    def total_return(self):
        """
        Calculate the total return of the backtest.

        :return: Total return as a percentage.
        """
        final_balance = self.history['Portfolio Value'].iloc[-1] if not self.history.empty else self.initial_balance
        total_return = (final_balance - self.initial_balance) / self.initial_balance * 100
        return total_return

    def annualized_return(self):
        """
        Calculate the annualized return of the backtest.

        :return: Annualized return as a percentage.
        """
        num_days = (self.end_date - self.start_date).days + 1
        total_return = self.history['Portfolio Value'].iloc[-1] / self.initial_balance - 1
        annualized_return = (1 + total_return) ** (365 / num_days) - 1
        return annualized_return * 100

    def sharpe_ratio(self, risk_free_rate=0.01):
        """
        Calculate the Sharpe Ratio of the backtest.

        :param risk_free_rate: Risk-free rate used for Sharpe Ratio calculation (annualized).
        :return: Sharpe Ratio.
        """
        returns = self.history['Profit'] / self.initial_balance if not self.history.empty else 0
        excess_returns = returns - risk_free_rate / 365.25  # Assuming daily returns
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else 0
        return sharpe_ratio

    def max_drawdown(self):
        """
        Calculate the maximum drawdown of the backtest.

        :return: Max drawdown as a percentage.
        """
        rolling_max = self.history['Portfolio Value'].cummax() if not self.history.empty else self.history['Portfolio Value']
        drawdown = (rolling_max - self.history['Portfolio Value']) / rolling_max if not rolling_max.empty else pd.Series([0])
        max_drawdown = drawdown.max() * 100
        return max_drawdown

    def calculate_all_metrics(self):
        """
        Calculate and return all metrics using fixed date range.

        :return: Dictionary of all calculated metrics.
        """
        num_days = (self.end_date - self.start_date).days + 1  # +1 to include both start and end dates
        num_years = num_days / 365  # Using a typical year length including leap years
        metrics = {
            'Total Return (%)': self.total_return(),
            'Annualized Return (%)': self.annualized_return(),
            'Sharpe Ratio': self.sharpe_ratio(),
            'Max Drawdown (%)': self.max_drawdown(),
            'Number of Years': num_years,
            'Number of Days' : num_days
        }
        return metrics

    def calculate_annual_returns(self):
        """
        Calculate annual returns based on the portfolio value.

        :return: List of annual returns as percentages.
        """
        assert 'Date' in self.history.columns, "Error: 'Date' column not found in history."
        num_days = (self.end_date - self.start_date).days + 1
        num_years = num_days / 365
        self.history['Date'] = pd.to_datetime(self.history['Date'])
        self.history.set_index('Date', inplace=True)
        self.history['Cumulative Balance'] = self.history['Profit'].cumsum() + self.initial_balance
        annual_returns = []

        for year, group in self.history.groupby(self.history.index.year):
            start_value = group['Cumulative Balance'].iloc[0]
            end_value = group['Cumulative Balance'].iloc[-1]
            annual_return = (end_value - start_value) / start_value * 100
            annual_returns.append(annual_return)

        return annual_returns, num_years
