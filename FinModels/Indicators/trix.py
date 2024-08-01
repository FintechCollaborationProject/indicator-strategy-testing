import pandas as pd
import numpy as np

class TRIX:
    def __init__(self, prices, short_window=12, long_window=24):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.trix_short = self.calculate_trix(self.short_window)
        self.trix_long = self.calculate_trix(self.long_window)
        self.signal_line = self.trix_short.ewm(span=self.short_window, adjust=False).mean()
    
    def calculate_trix(self, window):
        ema1 = self.prices['Close'].ewm(span=window, adjust=False).mean()
        ema2 = ema1.ewm(span=window, adjust=False).mean()
        ema3 = ema2.ewm(span=window, adjust=False).mean()
        trix = ((ema3 - ema3.shift(1)) / ema3.shift(1)) * 100
        return trix
    
    def cross_signal(self):
        buy_signal = (self.trix_short > self.signal_line).shift(1) & (self.trix_short <= self.signal_line)
        sell_signal = (self.trix_short < self.signal_line).shift(1) & (self.trix_short >= self.signal_line)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.trix_short > self.trix_long
        sell_signal = self.trix_short < self.trix_long
        return buy_signal, sell_signal
