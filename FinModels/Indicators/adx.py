import pandas as pd
import numpy as np

class ADX:
    def __init__(self, prices, window=14):
        if prices.empty:
            raise ValueError("Input data is empty.")
        self.prices = prices
        self.window = window
        self.adx = self.calculate_adx()
    
    def calculate_adx(self):
        high = self.prices['High']
        low = self.prices['Low']
        close = self.prices['Close']

        plus_dm = np.where((high.diff() > low.diff()) & (high.diff() > 0), high.diff(), 0)
        minus_dm = np.where((low.diff() > high.diff()) & (low.diff() > 0), low.diff(), 0)

        atr = (high.combine(low, max) - high.combine(low, min)).rolling(window=self.window).mean()

        plus_di = 100 * (plus_dm / atr).ewm(span=self.window, adjust=False).mean()
        minus_di = 100 * (minus_dm / atr).ewm(span=self.window, adjust=False).mean()

        dx = 100 * np.abs((plus_di - minus_di) / (plus_di + minus_di)).fillna(0)
        adx = dx.ewm(span=self.window, adjust=False).mean()
        
        return adx

    def aux_signal(self):
        buy_signal = self.adx > 25
        sell_signal = self.adx < 25
        return buy_signal, sell_signal
