import pandas as pd
import numpy as np

class MA:
    def __init__(self, prices, short_window=10, long_window=30):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.short_ma = self.calculate_ma(self.short_window)
        self.long_ma = self.calculate_ma(self.long_window)
    
    def calculate_ma(self, window):
        return self.prices['Close'].rolling(window).mean()
    
    def cross_signal(self):
        # Buy signal when the price crosses above the short MA and sell signal when it crosses below
        buy_signal = (self.prices['Close'] > self.short_ma).shift(1) & (self.prices['Close'] <= self.short_ma)
        sell_signal = (self.prices['Close'] < self.short_ma).shift(1) & (self.prices['Close'] >= self.short_ma)
        return buy_signal, sell_signal

    def aux_signal(self):
        # Buy signal when the short MA is above the long MA and sell signal when it's below
        buy_signal = self.short_ma > self.long_ma
        sell_signal = self.short_ma < self.long_ma
        return buy_signal, sell_signal
