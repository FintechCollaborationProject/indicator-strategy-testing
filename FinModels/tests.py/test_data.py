import unittest
from data.yahoo_finance_data import YahooFinanceData
from unittest.mock import patch

class TestYahooFinanceData(unittest.TestCase):
    @patch('data.yahoo_finance_data.YahooFinanceData.fetch_data')
    def test_data_fetch(self, mock_fetch):
        mock_fetch.return_value = {'price': 150}
        # Providing the required initialization arguments
        data = YahooFinanceData(ticker='AAPL', start_date='2022-01-01', end_date='2022-12-31').fetch_data('AAPL')
        self.assertIsNotNone(data)
        self.assertIn('price', data)
        self.assertEqual(data['price'], 150)

if __name__ == '__main__':
    unittest.main()
