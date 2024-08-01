import pandas as pd
import numpy as np

class KDJ:
    def __init__(self, prices, window=9):
        self.prices = prices
        self.window = window
        self.k, self.d, self.j = self.calculate_kdj()
    
    def calculate_kdj(self):
        low_min = self.prices['Low'].rolling(window=self.window).min()
        high_max = self.prices['High'].rolling(window=self.window).max()
        rsv = (self.prices['Close'] - low_min) / (high_max - low_min) * 100
        k = rsv.ewm(alpha=1/3, adjust=False).mean()
        d = k.ewm(alpha=1/3, adjust=False).mean()
        j = 3 * k - 2 * d
        return k, d, j
    
    def cross_signal(self):
        buy_signal = (self.k < self.d).shift(1) & (self.k >= self.d)
        sell_signal = (self.k > self.d).shift(1) & (self.k <= self.d)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.j < 20
        sell_signal = self.j > 80
        return buy_signal, sell_signal
