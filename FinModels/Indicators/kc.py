import pandas as pd
import numpy as np

class KC:
    def __init__(self, prices, window=20, multiplier=2):
        self.prices = prices
        self.window = window
        self.multiplier = multiplier
        self.middle_band, self.upper_band, self.lower_band = self.calculate_kc()
    
    def calculate_kc(self):
        high = self.prices['High']
        low = self.prices['Low']
        close = self.prices['Close']
        
        tr = pd.DataFrame({
            'H-L': high - low,
            'H-Ct1': np.abs(high - close.shift(1)),
            'L-Ct1': np.abs(low - close.shift(1))
        })
        tr['TR'] = tr.max(axis=1)
        atr = tr['TR'].rolling(window=self.window).mean()
        
        middle_band = close.rolling(window=self.window).mean()
        upper_band = middle_band + self.multiplier * atr
        lower_band = middle_band - self.multiplier * atr
        
        return middle_band, upper_band, lower_band

    def cross_signal(self):
        buy_signal = (self.prices['Close'] > self.lower_band).shift(1) & (self.prices['Close'] <= self.lower_band)
        sell_signal = (self.prices['Close'] < self.lower_band).shift(1) | (self.prices['Close'] > self.upper_band).shift(1)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.prices['Close'] < self.lower_band
        sell_signal = self.prices['Close'] > self.upper_band
        return buy_signal, sell_signal