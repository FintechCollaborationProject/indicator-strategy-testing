import pandas as pd
import numpy as np

class Backtest:
    def __init__(self, strategy, data, initial_balance):
        """
        Initialize the Backtest object.

        :param strategy: The trading strategy object that generates buy/sell signals.
        :param data: A DataFrame containing the market data.
        :param initial_balance: The starting balance for the backtest.
        """
        self.strategy = strategy
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # 0 means no position, 1 means long position
        self.history = []

    def execute(self):
        """
        Execute the backtest by iterating over the data and applying the strategy.

        :return: A DataFrame containing the backtest history with 'Date', 'Action', 'Price', and 'Profit' columns.
        """
        # Generate buy and sell signals using the provided strategy
        buy_signals, sell_signals = self.strategy.generate_signals()
        close_prices = self.data['Close']
        buy_price = None  # Track the buy price to calculate profit

        for i in range(len(close_prices)):
            date = close_prices.index[i]
            print(f"Date: {date}, Close Price: {close_prices.iloc[i]}")

            if buy_signals.iloc[i] and self.position == 0:
                # Execute buy action
                self.position = 1
                buy_price = close_prices.iloc[i]
                self.history.append({'Date': date, 'Action': 'Buy', 'Price': buy_price, 'Profit': 0})
                print(f"Buy at {buy_price} on {date}")

            elif sell_signals.iloc[i] and self.position == 1:
                # Execute sell action
                sell_price = close_prices.iloc[i]
                profit = (sell_price - buy_price) / buy_price * self.initial_balance
                self.balance += profit
                self.position = 0
                self.history.append({'Date': date, 'Action': 'Sell', 'Price': sell_price, 'Profit': profit})
                print(f"Sell at {sell_price} on {date}; Profit: {profit}")

            else:
                print("No action taken.")

        # Convert 'Date' to datetime and ensure 'Profit' column has numerical values
        history_df = pd.DataFrame(self.history)
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        history_df['Profit'] = history_df['Profit'].astype(float)

        print(f"Final balance: {self.balance}")
        return history_df

    #def annualized_return(self):
        """
        Calculate the annualized return of the backtest.

        :return: The annualized return as a percentage.
        """
        history_df = pd.DataFrame(self.history)
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        history_df.set_index('Date', inplace=True)
        
        num_days = (history_df.index[-1] - history_df.index[0]).days
        print(f"*****backtest number of days: {num_days}")

        if num_days > 0:
            total_return = (history_df['Profit'].sum() + self.initial_balance) / self.initial_balance
            annualized_return = (total_return ** (365 / num_days)) - 1
            return annualized_return * 100  # Convert to percentage
        else:
            return 0