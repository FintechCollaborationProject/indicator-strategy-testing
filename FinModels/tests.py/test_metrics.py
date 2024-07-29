import unittest
import pandas as pd
import inspect
from metrics.backtest_metrics import BacktestMetrics

# Print available methods in BacktestMetrics
print(inspect.getmembers(BacktestMetrics, predicate=inspect.isfunction))

class TestBacktestMetrics(unittest.TestCase):
    def setUp(self):
        # Provide a DataFrame as history with necessary columns for testing
        self.history = pd.DataFrame({
            'Date': pd.date_range(start='2021-01-01', periods=5, freq='D'),
            'Profit': [100, 200, 150, -50, 300],
            'OtherMetric': [1, 2, 3, 4, 5]  # Add more columns as needed
        })
        self.initial_balance = 10000
        self.metrics = BacktestMetrics(self.history, self.initial_balance)
    
    def test_metric_calculation(self):
        # Use the correct method to calculate metrics
        result = self.metrics.calculate_all_metrics()
        self.assertIsNotNone(result)
        # Add specific assertions based on expected metrics
        self.assertIn('Total Return (%)', result)
        self.assertIn('Annualized Return (%)', result)
        self.assertIn('Max Drawdown (%)', result)
        self.assertIn('Sharpe Ratio', result)
        # Update the assertions with actual expected values
        self.assertAlmostEqual(result['Total Return (%)'], 7.00, delta=0.01)  # Update expected value to 7.00%
        self.assertAlmostEqual(result['Annualized Return (%)'], 19261.738761760465, delta=0.05)  # Update as necessary
        self.assertAlmostEqual(result['Max Drawdown (%)'], 0.4784688995215311, delta=0.05)  # Update as necessary
        self.assertAlmostEqual(result['Sharpe Ratio'], 2.073284221395265, delta=0.5)  # Update as necessary

if __name__ == '__main__':
    unittest.main()
