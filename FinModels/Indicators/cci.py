import pandas as pd
import numpy as np

class CCI:
    def __init__(self, prices, window=20):
        self.prices = prices
        self.window = window
        self.cci = self.calculate_cci()
    
    def calculate_cci(self):
        tp = (self.prices['High'] + self.prices['Low'] + self.prices['Close']) / 3
        ma = tp.rolling(self.window).mean()
        md = tp.rolling(self.window).apply(lambda x: np.mean(np.abs(x - np.mean(x))))
        cci = (tp - ma) / (0.015 * md)
        return cci
    
    def aux_signal(self):
        buy_signal = self.cci < -100
        sell_signal = self.cci > 100
        return buy_signal, sell_signal