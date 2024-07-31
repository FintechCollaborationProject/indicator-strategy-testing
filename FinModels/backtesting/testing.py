import pandas as pd
import yfinance as yf

# Define the YahooFinanceData class
class YahooFinanceData:
    def __init__(self, ticker, start_date, end_date, interval='1d'):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(
                self.ticker,
                start=self.start_date,
                end=self.end_date,
                interval=self.interval
            )
            if not self.data.empty:
                print(f"Data fetched successfully for {self.ticker}")
            else:
                print(f"No data found for {self.ticker} in the given date range.")
        except Exception as e:
            print(f"An error occurred while fetching data for {self.ticker}: {e}")

    def get_data(self):
        if self.data is not None and not self.data.empty:
            return self.data
        else:
            print("Data not available. Please fetch data first.")
            return None

# Define the Backtest class
class Backtest:
    def __init__(self, strategy, data, initial_balance):
        self.strategy = strategy
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0
        self.history = []

    def execute(self):
        buy_signals, sell_signals = self.strategy.generate_signals()
        close_prices = self.data['Close']
        buy_price = None

        for i in range(len(close_prices)):
            date = close_prices.index[i]

            if buy_signals.iloc[i] and self.position == 0:
                self.position = 1
                buy_price = close_prices.iloc[i]
                self.history.append({'Date': date, 'Action': 'Buy', 'Price': buy_price, 'Profit': 0})

            elif sell_signals.iloc[i] and self.position == 1:
                sell_price = close_prices.iloc[i]
                profit = (sell_price - buy_price) / buy_price * self.initial_balance
                self.balance += profit
                self.position = 0
                self.history.append({'Date': date, 'Action': 'Sell', 'Price': sell_price, 'Profit': profit})

        history_df = pd.DataFrame(self.history)
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        history_df['Profit'] = history_df['Profit'].astype(float)

        return history_df

    def annualized_return(self):
        """
        Calculate the annualized return of the backtest.

        :return: The annualized return as a percentage.
        """
        history_df = pd.DataFrame(self.history)
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        history_df.set_index('Date', inplace=True)

        if not history_df.empty:
            first_date = self.data.index[0]
            last_date = self.data.index[-1]
            num_days = (last_date - first_date).days
            print(f"Number of days in backtest: {num_days}")

            if num_days > 0:
                total_return = (self.balance / self.initial_balance)
                annualized_return = (total_return ** (365 / num_days)) - 1
                return annualized_return * 100  # Convert to percentage
            else:
                return 0
        else:
            print("No trades executed in the backtest.")
            return 0

# Example usage
yahoo_data = YahooFinanceData("AAPL", "2020-01-01", "2021-01-01", "1d")
yahoo_data.fetch_data()
data = yahoo_data.get_data()
print(data.head())  # Print the first few rows of the data

# Define a simple strategy for demonstration purposes
class DummyStrategy:
    def generate_signals(self):
        close = data['Close']
        buy_signals = close > close.shift(1)  # Buy if price is going up
        sell_signals = close < close.shift(1)  # Sell if price is going down
        return buy_signals, sell_signals

strategy = DummyStrategy()
backtest = Backtest(strategy, data, 10000)
backtest.execute()
annualized_return = backtest.annualized_return()
print(f"Annualized Return: {annualized_return}%")
