from FinModels.Indicators import ADX, BollingerBands, EMA, KeltnerChannel, MACD, RSI, VortexIndicator
from FinModels.data.yahoo_finance_data import YahooFinanceData
from FinModels.strategies.combined_indicator_strategy import CombinedIndicatorStrategy
from FinModels.backtesting.backtest import Backtest
from FinModels.metrics import BacktestMetrics, ReturnAnalysis, TGR, CAGR
import pandas as pd
import yfinance as yf

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
            'VortexIndicator': VortexIndicator,
            'EMA': EMA,
            'RSI': RSI,
            'ADX': ADX,
            'BollingerBands': BollingerBands,
            'KeltnerChannel': KeltnerChannel,
            'MACD': MACD
        }

    def fetch_data(self):
        yahoo_data = YahooFinanceData(self.ticker, self.start_date, self.end_date, self.interval)
        yahoo_data.fetch_data()
        self.data = yahoo_data.get_data()
        if self.data is not None:
            self.data.index = pd.to_datetime(self.data.index)  # Convert the index to datetime format
            print("Data fetched:")
            print(self.data.head())  
            print("Columns in the data:")
            print(self.data.columns)
        else:
            print("No data fetched.")

    def initialize_indicators(self, indicators_to_use):
        indicators = []
        for indicator_name in indicators_to_use:
            indicator_class = self.indicator_classes.get(indicator_name)
            if indicator_class:
                if indicator_name == 'EMA':
                    indicators.append(indicator_class(self.data, short_window=5, long_window=10))
                elif indicator_name == 'BollingerBands':
                    indicators.append(indicator_class(self.data, window=20, num_std_dev=2))
                else:
                    indicators.append(indicator_class(self.data))
        self.strategy = CombinedIndicatorStrategy(indicators)

    def run_backtest(self):
        if self.data is not None and self.strategy is not None:
            backtest = Backtest(self.strategy, self.data, self.initial_balance)      
            backtest_history = backtest.execute()
            
            # Check if 'Date' is already in columns and if not, handle it
            if 'Date' not in backtest_history.columns and 'index' in backtest_history.columns:
                backtest_history.rename(columns={'index': 'Date'}, inplace=True)
            backtest_history.reset_index(inplace=True)
            
            # Remove any duplicate columns if present
            backtest_history = backtest_history.loc[:, ~backtest_history.columns.duplicated()]
            
            print("Backtest history data after processing:")
            print(backtest_history.head())
            print("Columns in backtest history:", backtest_history.columns)
            
            return backtest_history
        else:
            print("Data or Strategy not initialized.")
            return None

    def analyze_metrics(self, backtest_history):
        if backtest_history is not None and not backtest_history.empty:
            print("Backtest history data:")
            print(backtest_history.head())
            print("Columns in backtest history:", backtest_history.columns)
            metrics = BacktestMetrics(backtest_history, self.initial_balance)        

            all_metrics = metrics.calculate_all_metrics()
            annual_returns = metrics.calculate_annual_returns()
            return all_metrics, annual_returns
        else:
            print("Backtest history is None or empty.")
            return None, None

    def print_results(self, all_metrics, annual_returns):
        print("\nPerformance Metrics:")
        for key, value in all_metrics.items():
            print(f"{key}: {value:.2f}")

        print("\nAnnual Returns:")
        print(annual_returns)

        return_analysis = ReturnAnalysis(annual_returns)
        print("\nReturn Analysis Summary:")
        print(return_analysis.get_summary())

        tgr = TGR(annual_returns)
        print(f"\nTotal Growth Rate (TGR): {tgr.calculate():.2f}%")

        cagr = CAGR(annual_returns)
        print(f"Compound Annual Growth Rate (CAGR): {cagr.calculate():.2f}%")

def main():
    ticker = "GOOGL"
    start_date = "2022-06-01"
    end_date = "2023-01-01"
    interval = "1d"
    initial_balance = 100000
    indicators_to_use = ['BollingerBands', "RSI"]

    backtester = FinanceBacktester(ticker, start_date, end_date, interval, initial_balance)
    backtester.fetch_data()
    backtester.initialize_indicators(indicators_to_use)

    backtest_history = backtester.run_backtest()
    all_metrics, annual_returns = backtester.analyze_metrics(backtest_history)
    backtester.print_results(all_metrics, annual_returns)

if __name__ == "__main__":
    main()