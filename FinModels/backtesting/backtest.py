import pandas as pd

class Backtest:
    def __init__(self, strategy, data, initial_balance):
        self.strategy = strategy
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # 0 means no position, 1 means long position
        self.history = []

    # In the Backtest class
    def execute(self):
        buy_signals, sell_signals = self.strategy.generate_signals()
        close_prices = self.data['Close']
        buy_price = None  # Initialize buy_price to avoid scope issues

        for i in range(len(close_prices)):
            print(f"Date: {close_prices.index[i]}, Close Price: {close_prices.iloc[i]}")
            if buy_signals.iloc[i] and self.position == 0:
                # Buy action
                self.position = 1
                buy_price = close_prices.iloc[i]
                self.history.append({'Date': close_prices.index[i], 'Action': 'Buy', 'Price': buy_price})
                print(f"Buy at {buy_price} on {close_prices.index[i]}")
            elif sell_signals.iloc[i] and self.position == 1 and buy_price is not None:
                # Sell action
                self.position = 0
                sell_price = close_prices.iloc[i]
                profit = (sell_price - buy_price) / buy_price * self.initial_balance
                self.balance += profit
                self.history.append({'Date': close_prices.index[i], 'Action': 'Sell', 'Price': sell_price, 'Profit': profit})
                print(f"Sell at {sell_price} on {close_prices.index[i]}; Profit: {profit}")
            else:
                print("No action taken.")

        # Ensure 'Profit' column has numerical values only
        for entry in self.history:
            if 'Profit' not in entry:
                entry['Profit'] = 0

        print(f"Final balance: {self.balance}")
        return pd.DataFrame(self.history)

    # Ensure the index is datetime and correctly calculates days
    def annualized_return(self):
        self.history['Date'] = pd.to_datetime(self.history['Date'])
        self.history.set_index('Date', inplace=True)
        num_days = (self.history.index[-1] - self.history.index[0]).days
        return ((self.history['Profit'].sum() + self.initial_balance) / self.initial_balance) ** (365 / num_days) - 1

