import pandas as pd
import numpy as np

class ADX:
    def __init__(self, prices, window=14):
        self.prices = prices
        self.window = window
        self.adx, self.plus_di, self.minus_di = self.calculate_adx()
    
    def calculate_adx(self):
        high = self.prices['High']
        low = self.prices['Low']
        close = self.prices['Close']

        # Calculate True Range (TR)
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # Calculate +DI and -DI
        plus_dm = high.diff()
        minus_dm = low.diff()

        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0
        minus_dm = minus_dm.abs()

        tr_rolling = tr.rolling(window=self.window).sum()
        plus_di = 100 * (plus_dm.rolling(window=self.window).sum() / tr_rolling)
        minus_di = 100 * (minus_dm.rolling(window=self.window).sum() / tr_rolling)

        # Calculate DX
        dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))

        # Calculate ADX
        adx = dx.rolling(window=self.window).mean()

        return adx, plus_di, minus_di

    def aux_signal(self):
        buy_signal = (self.adx > 25) & (self.plus_di > self.minus_di)
        sell_signal = (self.adx > 25) & (self.minus_di > self.plus_di)
        return buy_signal, sell_signal