import pandas as pd
from Indicators import ADX, BB, EMA, KC, MACD, RSI, VI
from data.yahoo_finance_data import YahooFinanceData
from strategies.combined_indicator_strategy import CombinedIndicatorStrategy
from backtesting.backtest import Backtest
from metrics import BacktestMetrics, ReturnAnalysis, TGR, CAGR

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
        self._process_data()

    def _process_data(self):
        self.data.index = pd.to_datetime(self.data.index)
        self.data.reset_index(inplace=True)
        self.data.rename(columns={'index': 'Date'}, inplace=True)
        self._print_data_summary()

    def _print_data_summary(self):
        print("\nData fetched:")
        print(self.data.head())
        print("\nColumns in the data:")
        print(self.data.columns)

    def initialize_indicators(self, indicators_to_use):
        numeric_data = self.data.select_dtypes(include=['number'])
        indicators = [self._create_indicator(indicator_name, numeric_data) for indicator_name in indicators_to_use]
        self.strategy = CombinedIndicatorStrategy(indicators)

    def _create_indicator(self, indicator_name, numeric_data):
        indicator_class = self.indicator_classes.get(indicator_name)
        params = self._get_indicator_params(indicator_name)
        return indicator_class(numeric_data, **params) if indicator_name != 'EMA' else indicator_class(numeric_data, params['short_window'], params['long_window'])

    def _get_indicator_params(self, indicator_name):
        params = {
            'EMA': {'short_window': 12, 'long_window': 26},
            'BB': {'window': 20, 'num_std_dev': 2},
            'ADX': {'window': 14},
            'MACD': {'short_window': 12, 'long_window': 26, 'signal_window': 9},
            'RSI': {'window': 14},
            'KC': {'window': 20, 'multiplier': 2},
            'VI': {'window': 14}
        }
        return params.get(indicator_name, {})

    def run_backtest(self):
        backtest = Backtest(self.strategy, self.data, self.initial_balance)
        backtest_history = backtest.execute()
        return self._process_backtest_history(backtest_history)

    def _process_backtest_history(self, backtest_history):
        if len(backtest_history) <= len(self.data):
            backtest_history['Date'] = self.data['Date'].iloc[:len(backtest_history)]
        backtest_history['Date'] = pd.to_datetime(backtest_history['Date'])
        backtest_history.reset_index(drop=True, inplace=True)
        backtest_history = backtest_history.loc[:, ~backtest_history.columns.duplicated()]
        self._print_backtest_summary(backtest_history)
        return backtest_history

    def _print_backtest_summary(self, backtest_history):
        print("\nBacktest history data after processing:")
        print(backtest_history.head())
        print("\nColumns in backtest history:")
        print(backtest_history.columns)

    def analyze_metrics(self, backtest_history):
        backtest_history['Date'] = pd.to_datetime(backtest_history['Date'])
        metrics = BacktestMetrics(backtest_history, self.initial_balance, self.start_date, self.end_date)
        all_metrics = metrics.calculate_all_metrics()
        annual_returns = metrics.calculate_annual_returns()
        print(f"Annual Returns: {annual_returns}")
        return all_metrics, annual_returns

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

def configure_backtest():
    ticker = "AAPL"
    start_date = "2020-06-01"
    end_date = "2023-01-01"
    interval = "1d"
    initial_balance = 100000
    indicators_to_use = ["BB"]
    return ticker, start_date, end_date, interval, initial_balance, indicators_to_use 

def run():
    ticker, start_date, end_date, interval, initial_balance, indicators_to_use = configure_backtest()
    backtester = FinanceBacktester(ticker, start_date, end_date, interval, initial_balance)
    backtester.fetch_data()
    backtester.initialize_indicators(indicators_to_use)
    backtest_history = backtester.run_backtest()
    all_metrics, annual_returns = backtester.analyze_metrics(backtest_history)
    backtester.print_results(all_metrics, annual_returns)

if __name__ == "__main__":
    run()