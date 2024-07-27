import pandas as pd

class Backtest:
    def __init__(self, strategy, data, initial_balance):
        self.strategy = strategy
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # 0 means no position, 1 means long position
        self.history = []

    def execute(self):
        buy_signals, sell_signals = self.strategy.generate_signals()
        close_prices = self.data['Close']

        for i in range(len(close_prices)):
            if buy_signals.iloc[i] and self.position == 0:
                # Buy action
                self.position = 1
                buy_price = close_prices.iloc[i]
                self.history.append({'Date': close_prices.index[i], 'Action': 'Buy', 'Price': buy_price})
                print(f"Buy at {buy_price} on {close_prices.index[i]}")
            elif sell_signals.iloc[i] and self.position == 1:
                # Sell action
                self.position = 0
                sell_price = close_prices.iloc[i]
                profit = (sell_price - buy_price) / buy_price * self.initial_balance
                self.balance += profit
                self.history.append({'Date': close_prices.index[i], 'Action': 'Sell', 'Price': sell_price, 'Profit': profit})
                print(f"Sell at {sell_price} on {close_prices.index[i]}; Profit: {profit}")

        print(f"Final balance: {self.balance}")
        return pd.DataFrame(self.history)