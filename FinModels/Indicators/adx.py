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
        plus_dm = self.prices.diff().clip(lower=0)
        minus_dm = -self.prices.diff().clip(upper=0)
        atr = self.prices.rolling(window=self.window).apply(lambda x: np.max(x) - np.min(x), raw=True)
        plus_di = 100 * (plus_dm / atr).ewm(span=self.window, adjust=False).mean()
        minus_di = 100 * (minus_dm / atr).ewm(span=self.window, adjust=False).mean()
        dx = 100 * np.abs((plus_di - minus_di) / (plus_di + minus_di))
        adx = dx.ewm(span=self.window, adjust=False).mean()
        return adx

    def aux_signal(self):
        buy_signal = self.adx > 25
        sell_signal = self.adx < 25
        return buy_signal, sell_signal
