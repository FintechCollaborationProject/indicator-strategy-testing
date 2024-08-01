import pandas as pd
import numpy as np

class OBV:
    """
    On-Balance Volume (OBV) uses volume flow to predict changes in stock price.
    It adds volume on up days and subtracts volume on down days to measure buying and selling pressure.
    """
    def __init__(self, prices):
        self.prices = prices
        self.obv = self.calculate_obv()
    
    def calculate_obv(self):
        obv = (np.sign(self.prices['Close'].diff()) * self.prices['Volume']).cumsum()
        return obv
    
    def aux_signal(self):
        buy_signal = self.obv > 0
        sell_signal = self.obv < 0
        return buy_signal, sell_signal