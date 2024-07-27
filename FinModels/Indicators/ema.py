import numpy as np
import pandas as pd

class EMA:
    def __init__(self, prices, short_window=5, long_window=10):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.short_ema = self.calculate_ema(short_window)
        self.long_ema = self.calculate_ema(long_window)
    
    def calculate_ema(self, window):
        return self.prices.ewm(span=window, adjust=False).mean()

    def cross_signal(self):
        buy_signal = (self.short_ema > self.long_ema) & (self.short_ema.shift(1) <= self.long_ema.shift(1))
        sell_signal = (self.short_ema < self.long_ema) & (self.short_ema.shift(1) >= self.long_ema.shift(1))
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.short_ema > self.long_ema
        sell_signal = self.short_ema < self.long_ema
        return buy_signal, sell_signal