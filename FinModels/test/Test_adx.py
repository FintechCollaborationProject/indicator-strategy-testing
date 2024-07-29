import unittest
import numpy as np
import pandas as pd
from Indicators.adx import ADX

class TestADX(unittest.TestCase):
    def setUp(self):
        # Sample data
        self.data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    def test_adx_calculation_basic(self):
        adx = ADX(self.data)
        result = adx.calculate_adx()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.data))

    def test_adx_with_empty_data(self):
        with self.assertRaises(ValueError):
            ADX(pd.Series([]))
    
    def test_adx_with_single_data_point(self):
        adx = ADX(pd.Series([1]))
        result = adx.calculate_adx()
        self.assertTrue(result.isnull().all())  # ADX cannot be calculated with insufficient data

    def test_aux_signal(self):
        adx = ADX(self.data)
        buy_signal, sell_signal = adx.aux_signal()
        self.assertEqual(len(buy_signal), len(self.data))
        self.assertEqual(len(sell_signal), len(self.data))
        self.assertTrue(isinstance(buy_signal, pd.Series) and isinstance(sell_signal, pd.Series))

    def test_aux_signal_thresholds(self):
        adx_values = pd.Series([10, 20, 25, 30, 40, 10])
        adx = ADX(adx_values)
        adx.adx = adx_values  # Mocking ADX values for this test
        buy_signal, sell_signal = adx.aux_signal()
        self.assertTrue(all(buy_signal == (adx_values > 25)))
        self.assertTrue(all(sell_signal == (adx_values < 25)))

if __name__ == '__main__':
    unittest.main()
