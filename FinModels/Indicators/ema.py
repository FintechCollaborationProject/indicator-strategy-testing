import pandas as pd

class EMA:
    def __init__(self, prices, short_window, long_window):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.short_ema, self.long_ema = self.calculate_emas()

    def calculate_emas(self):
        short_ema = self.prices['Close'].ewm(span=self.short_window, adjust=False).mean()
        long_ema = self.prices['Close'].ewm(span=self.long_window, adjust=False).mean()
        return short_ema, long_ema

    def cross_signal(self):
        buy_signal = (self.short_ema > self.long_ema) & (self.short_ema.shift(1) <= self.long_ema.shift(1))
        sell_signal = (self.short_ema < self.long_ema) & (self.short_ema.shift(1) >= self.long_ema.shift(1))
        return buy_signal, sell_signal
    
    def aux_signal(self):
        buy_signal = self.short_ema > self.long_ema
        sell_signal = self.short_ema < self.long_ema
        return buy_signal, sell_signal


