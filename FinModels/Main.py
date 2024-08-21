import pandas as pd
import itertools
from Indicators import (
    ADI, ADX, BB, CCI, DEMA, DPO, EMA, EMV, KC, KDJ, MA, MACD, MAE, MFI, MOM, OBV,
    OSC, PSAR, REX, RMA, RSI, TEMA, TRIX, UO, VI, WPR
)
from data.yahoo_finance_data import YahooFinanceData
from strategies.combined_indicator_strategy import CombinedIndicatorStrategy
from strategies.indicator_combinations import TradingIndicatorCombinations
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
            'ADI': ADI, 'ADX': ADX, 'BB': BB, 'CCI': CCI, 'DEMA': DEMA,
            'DPO': DPO, 'EMA': EMA, 'EMV': EMV, 'KC': KC, 'KDJ': KDJ, 'MA': MA,
            'MACD': MACD, 'MAE': MAE, 'MFI': MFI, 'MOM': MOM, 'OBV': OBV,
            'OSC': OSC, 'PSAR': PSAR, 'REX': REX, 'RMA': RMA, 'RSI': RSI,
            'TEMA': TEMA, 'TRIX': TRIX, 'UO': UO, 'VI': VI, 'WPR': WPR
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
            'ADI': {},  # Add specific parameters if needed
            'ADX': {'window': 14},
            'BB': {'window': 20, 'num_std_dev': 2},
            'CCI': {'window': 20},
            'DEMA': {'short_window': 10, 'long_window': 20},
            'DPO': {'window': 10},
            'EMA': {'short_window': 5, 'medium_window': 10, 'long_window': 30},
            'EMV': {'window': 9},
            'KC': {'window': 20, 'multiplier': 2},
            'KDJ': {'window': 9},
            'MA': {'short_window': 10, 'long_window': 30},
            'MACD': {'short_window': 12, 'long_window': 26, 'signal_window': 9},
            'MAE': {'window': 20, 'k': 3},
            'MFI': {'n1': 14, 'n2': 9},
            'MOM': {'window': 14},
            'OBV': {},  # No specific parameters needed
            'OSC': {'short_window': 12, 'long_window': 26},
            'PSAR': {'af_increment': 0.02, 'af_max': 0.2},
            'REX': {'short_window': 2, 'long_window': 10},
            'RMA': {'short_window': 10, 'long_window': 30},
            'RSI': {'window': 14},
            'TEMA': {'short_window': 10, 'long_window': 30},
            'TRIX': {'short_window': 12, 'long_window': 24},
            'UO': {'n1': 7, 'n2': 14, 'n3': 28, 'ns': 3, 'nl': 7},
            'VI': {'window': 14},
            'WPR': {'window': 14}
        }
        return params.get(indicator_name, {})

    def run_backtest(self):
        backtest = Backtest(self.strategy, self.data, self.initial_balance)
        backtest_history = backtest.execute()
        return self._process_backtest_history(backtest_history)

    def run_buy_and_hold(self):
        initial_bh, final_bh = self.buy_and_hold()
        print(f"Buy and Hold Strategy: Initial = ${initial_bh:.2f}, Final = ${final_bh:.2f}, Return = ${(final_bh - initial_bh):.2f}")

    def buy_and_hold(self):
        if self.data is None or self.data.empty:
            print("No data available for Buy and Hold strategy.")
            return None, None

        buy_price = self.data['Close'].iloc[0]
        position = self.initial_balance // buy_price
        cash = self.initial_balance - position * buy_price
        final_value = cash + position * self.data['Close'].iloc[-1]
        return self.initial_balance, final_value

    def _process_backtest_history(self, backtest_history):
        if len(backtest_history) <= len(self.data):
            backtest_history['Date'] = self.data['Date'].iloc[:len(backtest_history)]
        backtest_history['Date'] = pd.to_datetime(backtest_history['Date'])
        backtest_history.reset_index(drop=True, inplace=True)
        backtest_history = backtest_history.loc[:, ~backtest_history.columns.duplicated()]
        return backtest_history

    def analyze_metrics(self, backtest_history):
        backtest_history['Date'] = pd.to_datetime(backtest_history['Date'])
        metrics = BacktestMetrics(backtest_history, self.initial_balance, self.start_date, self.end_date)
        all_metrics = metrics.calculate_all_metrics()
        annual_returns, num_years = metrics.calculate_annual_returns()
        return all_metrics, annual_returns, num_years

    def print_results(self, all_metrics, annual_returns, num_years):
        print("\nPerformance Metrics:")
        for key, value in all_metrics.items():
            print(f"{key}: {value:.2f}")
        print("\nAnnual Returns:")
        print(annual_returns)
        return_analysis = ReturnAnalysis(annual_returns, num_years)
        print("\nReturn Analysis Summary:")
        print(return_analysis.get_summary())
        tgr = TGR(annual_returns)
        print(f"\nTotal Growth Rate (TGR): {tgr.calculate():.2f}%")
        cagr = CAGR(annual_returns, num_years)
        print(f"Compound Annual Growth Rate (CAGR): {cagr.calculate():.2f}%")

def configure_backtest():
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2024-01-01"
    interval = "1d"
    initial_balance = 100000

    # Classification of Indicators:
    # arg for indicators_to_use = [Cross & AUX, AUX or Cross & AUX , AUX or Cross & AUX]
    # Cross & AUX: BB, DEMA, EMA, EMV, KC, KDJ, MA, MACD, MFI, REX, RMA, TEMA, TRIX, UO, VI
    # AUX: ADI, ADX, CCI, DPO, MAE, MOM, OBV, OSC, PSAR, RSI, WPR
    
    # indicators_to_use = ["BB"] #This can be modified to other combinations as well
    # indicators_to_use = ["DEMA", "RSI"]
    # indicators_to_use = ["MA", "CCI", "ADX"]
    # indicators_to_use = ["ALL"]
    # indicators_to_use = ["Cross & AUX", "AUX", "none"]
    # indicators_to_use = ["Cross & AUX", "Cross & AUX", "AUX"]
    # indicators_to_use = ["Cross & AUX", "Cross & AUX", "Cross & AUX"]
    # indicators_to_use = ["Cross & AUX", "AUX", "AUX"]
    # indicators_to_use = ["Cross & AUX", "AUX", "none"]
    indicators_to_use = ["Cross & AUX", "none", "none"]
    strategy = "buy_and_hold"
    return ticker, start_date, end_date, interval, initial_balance, indicators_to_use, strategy

def run():
    ticker, start_date, end_date, interval, initial_balance, indicators_to_use, strategy = configure_backtest()
    backtester = FinanceBacktester(ticker, start_date, end_date, interval, initial_balance)
    backtester.fetch_data()
    backtester.run_buy_and_hold()

    # Generate or use predefined combinations of indicators
    if indicators_to_use == ["ALL"] or "Cross & AUX" in indicators_to_use:
        tic = TradingIndicatorCombinations(indicators_to_use)
        indicator_combinations = tic.generate_combinations()
    else:
        indicator_combinations = [indicators_to_use]

    # Run backtest for each combination
    for combo in indicator_combinations:
        print(f"\nRunning backtest for combination: {combo}")
        try:
            backtester.initialize_indicators(combo)
            backtest_history = backtester.run_backtest()
            all_metrics, annual_returns, num_years = backtester.analyze_metrics(backtest_history)
            backtester.print_results(all_metrics, annual_returns, num_years)
        except ValueError as e:
            print(f"Skipping combination {combo} due to error: {e}")

if __name__ == "__main__":
    run()
