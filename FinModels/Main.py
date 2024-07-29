import pandas as pd
from Indicators import ADX, BB, EMA, KC, MACD, RSI, VI
from data.yahoo_finance_data import YahooFinanceData
from strategies.combined_indicator_strategy import CombinedIndicatorStrategy
from backtesting.backtest import Backtest
from metrics import BacktestMetrics, ReturnAnalysis, TGR, CAGR
import numpy as np

class FinanceBacktester:
    def __init__(self, ticker, start_date, end_date, interval, initial_balance):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.initial_balance = initial_balance
        self.data = None
        self.strategy = None
        self.indicator_classes = {
            'VI': VI,
            'EMA': EMA,
            'RSI': RSI,
            'ADX': ADX,
            'BB': BB,
            'KC': KC,
            'MACD': MACD
        }

    def fetch_data(self):
        yahoo_data = YahooFinanceData(self.ticker, self.start_date, self.end_date, self.interval)
        yahoo_data.fetch_data()
        self.data = yahoo_data.get_data()
        if self.data is not None and not self.data.empty:
            self._process_data()
        else:
            print("No data fetched.")

    def _process_data(self):
        self.data.index = pd.to_datetime(self.data.index)
        self.data.reset_index(inplace=True)
        self.data.rename(columns={'index': 'Date'}, inplace=True)
        print("\nData fetched:")
        print(self.data.head())
        print("\nColumns in the data:")
        print(self.data.columns)

    def initialize_indicators(self, indicators_to_use):
        numeric_data = self.data.select_dtypes(include=['number'])
        indicators = []
        for indicator_name in indicators_to_use:
            indicator_class = self.indicator_classes.get(indicator_name)
            if indicator_class:
                params = self._get_indicator_params(indicator_name)
                # Adjust the instantiation if the number of parameters differs
                indicators.append(indicator_class(numeric_data, **params))
            else:
                print(f"Warning: Indicator '{indicator_name}' not found.")
        self.strategy = CombinedIndicatorStrategy(indicators)

    def _get_indicator_params(self, indicator_name):
        params = {
            'EMA': {'short_window': 5, 'long_window': 10},
            'BB': {'window': 20, 'num_std_dev': 2}
        }
        return params.get(indicator_name, {})

    def run_backtest(self):
        if self.data is not None and self.strategy is not None:
            backtest = Backtest(self.strategy, self.data, self.initial_balance)
            backtest_history = backtest.execute()
            backtest_history = self._process_backtest_history(backtest_history)
            return backtest_history
        else:
            print("Data or Strategy not initialized.")
            return None

    def _process_backtest_history(self, backtest_history):
        if backtest_history is not None:
            if len(backtest_history) <= len(self.data):
                backtest_history['Date'] = self.data['Date'].iloc[:len(backtest_history)]
            else:
                print("Warning: Mismatch in the length of original data and backtest history.")
            if not pd.api.types.is_datetime64_any_dtype(backtest_history['Date']):
                backtest_history['Date'] = pd.to_datetime(backtest_history['Date'])
            backtest_history.reset_index(drop=True, inplace=True)
            backtest_history = backtest_history.loc[:, ~backtest_history.columns.duplicated()]
            print("\nBacktest history data after processing:")
            print(backtest_history.head())
            print("\nColumns in backtest history:")
            print(backtest_history.columns)
        return backtest_history

    def analyze_metrics(self, backtest_history):
        if backtest_history is not None and not backtest_history.empty:
            if 'Date' in backtest_history.columns:
                backtest_history['Date'] = pd.to_datetime(backtest_history['Date'])
            else:
                print("Error: 'Date' column is missing in backtest history.")
                return None, None

            metrics = BacktestMetrics(backtest_history, self.initial_balance)
            all_metrics = metrics.calculate_all_metrics()
            annual_returns = metrics.calculate_annual_returns()

            if len(annual_returns) == 0:
                print("No annual returns data available.")
                return all_metrics, None

            return all_metrics, annual_returns
        else:
            print("Backtest history is None or empty.")
            return None, None

    def print_results(self, all_metrics, annual_returns):
        print("\nPerformance Metrics:")
        if all_metrics:
            for key, value in all_metrics.items():
                print(f"{key}: {value:.2f}")
        else:
            print("No performance metrics available.")

        print("\nAnnual Returns:")
        if annual_returns is not None:
            print(annual_returns)
            return_analysis = ReturnAnalysis(annual_returns)
            print("\nReturn Analysis Summary:")
            print(return_analysis.get_summary())
            tgr = TGR(annual_returns)
            print(f"\nTotal Growth Rate (TGR): {tgr.calculate():.2f}%")
            cagr = CAGR(annual_returns)
            print(f"Compound Annual Growth Rate (CAGR): {cagr.calculate():.2f}%")
        else:
            print("No annual returns data available.")

def main():
    ticker = "BTC-USD"
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    interval = "1d"
    initial_balance = 100000
    indicators_to_use = ["VI"]
    
    backtester = FinanceBacktester(ticker, start_date, end_date, interval, initial_balance)
    backtester.fetch_data()
    backtester.initialize_indicators(indicators_to_use)
    backtest_history = backtester.run_backtest()
    all_metrics, annual_returns = backtester.analyze_metrics(backtest_history)
    backtester.print_results(all_metrics, annual_returns)

if __name__ == "__main__":
    main()
