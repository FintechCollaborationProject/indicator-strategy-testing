import pandas as pd
import numpy as np

class BacktestMetrics:
    def __init__(self, history, initial_balance):
        """
        Initialize the BacktestMetrics object.

        :param history: DataFrame containing the backtest trade history.
        :param initial_balance: The initial balance of the portfolio at the start of the backtest.
        """
        self.history = history
        self.initial_balance = initial_balance

    def total_return(self):
        """
        Calculate the total return from the backtest.

        :return: Total return as a percentage.
        """
        if self.history.empty:
            print("Warning: History is empty. Returning 0 for total return.")
            return 0  # or another appropriate value or raise an exception
        final_balance = self.history.iloc[-1]['Profit'] + self.initial_balance
        total_return = (final_balance - self.initial_balance) / self.initial_balance * 100
        return total_return

    def annualized_return(self):
        """
        Calculate the annualized return.

        :return: Annualized return as a percentage.
        """
        num_days = (self.history['Date'].iloc[-1] - self.history['Date'].iloc[0]).days
        total_return = self.total_return() / 100
        annualized_return = (1 + total_return) ** (365 / num_days) - 1
        return annualized_return * 100

    def sharpe_ratio(self, risk_free_rate=0.01):
        """
        Calculate the Sharpe Ratio.

        :param risk_free_rate: The risk-free rate, default is 0.01 (1%).
        :return: Sharpe Ratio.
        """
        returns = self.history['Profit'] / self.initial_balance
        excess_returns = returns - risk_free_rate / len(self.history)
        sharpe_ratio = np.sqrt(len(returns)) * excess_returns.mean() / excess_returns.std()
        return sharpe_ratio

    def max_drawdown(self):
        """
        Calculate the maximum drawdown.

        :return: Maximum drawdown as a percentage.
        """
        balance = self.history['Profit'].cumsum() + self.initial_balance
        drawdown = (balance.cummax() - balance) / balance.cummax()
        max_drawdown = drawdown.max() * 100
        return max_drawdown

    def calculate_all_metrics(self):
        """
        Calculate all metrics and return as a dictionary.

        :return: Dictionary of all performance metrics.
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
        Calculate the annual returns based on the trade history.

        :return: List of annual returns as percentages.
        """
        # Ensure the 'Date' column is a datetime type
        self.history['Date'] = pd.to_datetime(self.history['Date'])
        
        # Calculate cumulative balance over time
        self.history['Cumulative Balance'] = self.history['Profit'].cumsum() + self.initial_balance
        
        # Group by year and calculate annual return
        annual_returns = []
        for year, group in self.history.groupby(self.history['Date'].dt.year):
            start_value = group['Cumulative Balance'].iloc[0]
            end_value = group['Cumulative Balance'].iloc[-1]
            annual_return = (end_value - start_value) / start_value * 100
            annual_returns.append(annual_return)
        
        return annual_returns