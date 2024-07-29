import pandas as pd
import numpy as np

class KC:
    def __init__(self, prices, window=20, multiplier=2):
        self.prices = prices
        self.window = window
        self.multiplier = multiplier
        self.middle_band, self.upper_band, self.lower_band = self.calculate_bands()

    def calculate_atr(self):
        high_low = self.prices['High'] - self.prices['Low']
        high_close_prev = np.abs(self.prices['High'] - self.prices['Close'].shift(1))
        low_close_prev = np.abs(self.prices['Low'] - self.prices['Close'].shift(1))
        true_range = pd.DataFrame([high_low, high_close_prev, low_close_prev]).max()
        atr = true_range.rolling(window=self.window).mean()
        return atr

    def calculate_bands(self):
        middle_band = self.prices['Close'].ewm(span=self.window, adjust=False).mean()
        atr = self.calculate_atr()
        upper_band = middle_band + (atr * self.multiplier)
        lower_band = middle_band - (atr * self.multiplier)
        return middle_band, upper_band, lower_band

    def cross_signal(self):
        buy_signal = (self.prices['Close'] > self.lower_band).shift(1) & (self.prices['Close'] <= self.lower_band)
        sell_signal = (self.prices['Close'] < self.upper_band).shift(1) & (self.prices['Close'] >= self.upper_band)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.prices['Close'] < self.lower_band
        sell_signal = self.prices['Close'] > self.upper_band
        return buy_signal, sell_signal
