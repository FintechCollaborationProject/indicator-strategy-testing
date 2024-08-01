import pandas as pd
import numpy as np

class MOM:
    """
    Momentum (MOM) indicator measures the speed of price changes.
    It helps in identifying overbought or oversold conditions and potential trend reversals.
    """
    def __init__(self, prices, window=14):
        self.prices = prices
        self.window = window
        self.mom = self.calculate_mom()
    
    def calculate_mom(self):
        mom = self.prices['Close'] - self.prices['Close'].shift(self.window)
        return mom
    
    def aux_signal(self):
        buy_signal = self.mom > 0
        sell_signal = self.mom < 0
        return buy_signal, sell_signal