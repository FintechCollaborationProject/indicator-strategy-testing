import pandas as pd
import numpy as np

class DEMA:
    def __init__(self, prices, short_window=10, long_window=20):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.short_dema, self.long_dema = self.calculate_dema()
    
    def calculate_dema(self):
        # Short period DEMA
        ema1_short = self.prices['Close'].ewm(span=self.short_window, adjust=False).mean()
        ema2_short = ema1_short.ewm(span=self.short_window, adjust=False).mean()
        short_dema = 2 * ema1_short - ema2_short
        
        # Long period DEMA
        ema1_long = self.prices['Close'].ewm(span=self.long_window, adjust=False).mean()
        ema2_long = ema1_long.ewm(span=self.long_window, adjust=False).mean()
        long_dema = 2 * ema1_long - ema2_long
        
        return short_dema, long_dema
    
    def cross_signal(self):
        # Buy signal when price crosses above both short and long DEMA
        buy_signal = (self.prices['Close'] > self.short_dema).shift(1) & (self.prices['Close'] <= self.short_dema) | \
                     (self.prices['Close'] > self.long_dema).shift(1) & (self.prices['Close'] <= self.long_dema)
        # Sell signal when price crosses below both short and long DEMA
        sell_signal = (self.prices['Close'] < self.short_dema).shift(1) & (self.prices['Close'] >= self.short_dema) | \
                      (self.prices['Close'] < self.long_dema).shift(1) & (self.prices['Close'] >= self.long_dema)
        return buy_signal, sell_signal

    def aux_signal(self):
        # Buy signal when price is above both short and long DEMA
        buy_signal = (self.prices['Close'] > self.short_dema) & (self.prices['Close'] > self.long_dema)
        # Sell signal when price is below both short and long DEMA
        sell_signal = (self.prices['Close'] < self.short_dema) & (self.prices['Close'] < self.long_dema)
        return buy_signal, sell_signal
