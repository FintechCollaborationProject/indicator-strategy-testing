import pandas as pd

class RSI:
    def __init__(self, prices, window=14):
        self.prices = prices
        self.window = window
        self.rsi = self.calculate_rsi()
    
    def calculate_rsi(self):
        delta = self.prices['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(self.window).mean()
        avg_loss = loss.rolling(self.window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def aux_signal(self):
        buy_signal = self.rsi < 30
        sell_signal = self.rsi > 70
        return buy_signal, sell_signal
