import unittest
import pandas as pd
from Indicators.adx import ADX
from Indicators.rsi import RSI

class TestIndicators(unittest.TestCase):
    def setUp(self):
        # Create a pandas Series or DataFrame with mock data
        self.data = pd.Series([1, 2, 3, 4, 5])
        
    def test_adx_calculation(self):
        adx = ADX(self.data)
        result = adx.calculate_adx()
        self.assertIsNotNone(result)
        # Add more assertions to validate the result, e.g., type, range, etc.
    
    def test_rsi_calculation(self):
        rsi = RSI(self.data)
        result = rsi.calculate_rsi()
        self.assertIsNotNone(result)
        # Add more assertions to validate the result

if __name__ == '__main__':
    unittest.main()
