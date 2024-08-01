import pandas as pd
import numpy as np

class OSC:
    def __init__(self, prices, short_window=12, long_window=26):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.osc = self.calculate_osc()
    
    def calculate_osc(self):
        short_ema = self.prices['Close'].ewm(span=self.short_window, adjust=False).mean()
        long_ema = self.prices['Close'].ewm(span=self.long_window, adjust=False).mean()
        osc = short_ema - long_ema
        return osc
    
    def aux_signal(self):
        buy_signal = self.osc > 0
        sell_signal = self.osc < 0
        return buy_signal, sell_signal