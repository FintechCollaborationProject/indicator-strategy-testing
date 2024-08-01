import pandas as pd

class MACD:
    def __init__(self, prices, short_window=12, long_window=26, signal_window=9):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.dif, self.dea = self.calculate_macd()
    
    def calculate_macd(self):
        short_ema = self.prices['Close'].ewm(span=self.short_window, adjust=False).mean()
        long_ema = self.prices['Close'].ewm(span=self.long_window, adjust=False).mean()
        dif = short_ema - long_ema
        dea = dif.ewm(span=self.signal_window, adjust=False).mean()
        return dif, dea
    
    def cross_signal(self):
        buy_signal = (self.dif > self.dea).shift(1) & (self.dif <= self.dea)
        sell_signal = (self.dif < self.dea).shift(1) & (self.dif >= self.dea)
        return buy_signal, sell_signal

    def aux_signal(self):
        ma_10 = self.prices['Close'].rolling(window=10).mean()
        ma_30 = self.prices['Close'].rolling(window=30).mean()
        buy_signal = ma_10 > ma_30
        sell_signal = ma_10 < ma_30
        return buy_signal, sell_signal
