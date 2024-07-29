import unittest
from backtesting.backtest import Backtest
from unittest.mock import MagicMock

class TestBacktest(unittest.TestCase):
    def setUp(self):
        # Set up necessary data or mocks
        self.mock_strategy = MagicMock()
        self.mock_data = MagicMock()
        self.initial_balance = 100000  # Example initial balance
    
    def test_backtest_initialization(self):
        bt = Backtest(self.mock_data, self.mock_strategy, self.initial_balance)
        self.assertIsInstance(bt, Backtest)
    
    def test_backtest_run(self):
        bt = Backtest(self.mock_data, self.mock_strategy, self.initial_balance)
        bt.run = MagicMock(return_value='results')
        result = bt.run()
        self.assertEqual(result, 'results')

if __name__ == '__main__':
    unittest.main()
