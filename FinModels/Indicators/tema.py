import pandas as pd
import numpy as np

class TEMA:
    def __init__(self, prices, short_window=10, long_window=30):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.short_tema, self.long_tema = self.calculate_temas()
    
    def calculate_tema(self, n):
        ema1 = self.prices['Close'].ewm(span=n, adjust=False).mean()
        ema2 = ema1.ewm(span=n, adjust=False).mean()
        ema3 = ema2.ewm(span=n, adjust=False).mean()
        tema = 3 * ema1 - 3 * ema2 + ema3
        return tema
    
    def calculate_temas(self):
        short_tema = self.calculate_tema(self.short_window)
        long_tema = self.calculate_tema(self.long_window)
        return short_tema, long_tema
    
    def cross_signal(self):
        # Using short TEMA for cross signals
        buy_signal = (self.prices['Close'] > self.short_tema).shift(1) & (self.prices['Close'] <= self.short_tema)
        sell_signal = (self.prices['Close'] < self.short_tema).shift(1) & (self.prices['Close'] >= self.short_tema)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.short_tema > self.long_tema
        sell_signal = self.short_tema < self.long_tema
        return buy_signal, sell_signal
