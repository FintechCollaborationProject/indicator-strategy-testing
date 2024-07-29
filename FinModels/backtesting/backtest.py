
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
        buy_price = None  # Initialize buy_price to avoid scope issues

        for i in range(len(close_prices)):
            date = close_prices.index[i]
            print(f"Date: {date}, Close Price: {close_prices.iloc[i]}")
            if buy_signals.iloc[i] and self.position == 0:
                # Buy action
                self.position = 1
                buy_price = close_prices.iloc[i]
                self.history.append({'Date': date, 'Action': 'Buy', 'Price': buy_price, 'Profit': 0})
                print(f"Buy at {buy_price} on {date}")
            elif sell_signals.iloc[i] and self.position == 1 and buy_price is not None:
                # Sell action
                self.position = 0
                sell_price = close_prices.iloc[i]
                profit = (sell_price - buy_price) / buy_price * self.initial_balance
                self.balance += profit
                self.history.append({'Date': date, 'Action': 'Sell', 'Price': sell_price, 'Profit': profit})
                print(f"Sell at {sell_price} on {date}; Profit: {profit}")
            else:
                print("No action taken.")

        # Convert 'Date' to datetime and ensure 'Profit' column has numerical values only
        history_df = pd.DataFrame(self.history)
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        history_df['Profit'] = history_df['Profit'].astype(float)
        
        print(f"Final balance: {self.balance}")
        return history_df

    def annualized_return(self):
        self.history['Date'] = pd.to_datetime(self.history['Date'])
        self.history.set_index('Date', inplace=True)
        num_days = (self.history.index[-1] - self.history.index[0]).days
        if num_days > 0:
            return ((self.history['Profit'].sum() + self.initial_balance) / self.initial_balance) ** (365 / num_days) - 1
        else:
            return 0

    def max_drawdown(self):
        running_max = self.history['Portfolio Value'].cummax()
        drawdown = (self.history['Portfolio Value'] - running_max) / running_max
        return drawdown.min()
