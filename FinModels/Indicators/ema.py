import pandas as pd

class EMA:
    def __init__(self, prices, short_window=5, medium_window=10, long_window=30):
        self.prices = prices
        self.short_window = short_window
        self.medium_window = medium_window
        self.long_window = long_window
        self.short_ema = self.calculate_ema(self.short_window)
        self.medium_ema = self.calculate_ema(self.medium_window)
        self.long_ema = self.calculate_ema(self.long_window)
    
    def calculate_ema(self, window):
        return self.prices['Close'].ewm(span=window, adjust=False).mean()
    
    def cross_signal(self):
        buy_signal_5_10 = (self.short_ema > self.medium_ema).shift(1) & (self.short_ema <= self.medium_ema)
        sell_signal_5_10 = (self.short_ema < self.medium_ema).shift(1) & (self.short_ema >= self.medium_ema)
        
        buy_signal_10_30 = (self.medium_ema > self.long_ema).shift(1) & (self.medium_ema <= self.long_ema)
        sell_signal_10_30 = (self.medium_ema < self.long_ema).shift(1) & (self.medium_ema >= self.long_ema)
        
        return (buy_signal_5_10 | buy_signal_10_30), (sell_signal_5_10 | sell_signal_10_30)
    
    def aux_signal(self):
        buy_signal = self.medium_ema > self.long_ema
        sell_signal = self.medium_ema < self.long_ema
        return buy_signal, sell_signal
