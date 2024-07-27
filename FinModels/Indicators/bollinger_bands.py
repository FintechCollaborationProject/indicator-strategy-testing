import numpy as np
import pandas as pd

class BollingerBands:
    def __init__(self, prices, window=20, num_std_dev=2):
        self.prices = prices
        self.window = window
        self.num_std_dev = num_std_dev
        self.middle_band, self.upper_band, self.lower_band = self.calculate_bands()
    
    def calculate_bands(self):
        middle_band = self.prices.rolling(self.window).mean()
        std_dev = self.prices.rolling(self.window).std()
        upper_band = middle_band + (std_dev * self.num_std_dev)
        lower_band = middle_band - (std_dev * self.num_std_dev)
        return middle_band, upper_band, lower_band

    def cross_signal(self):
        buy_signal = (self.prices > self.lower_band).shift(1) & (self.prices <= self.lower_band)
        sell_signal = (self.prices < self.lower_band) | (self.prices > self.upper_band)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.prices < self.lower_band
        sell_signal = self.prices > self.upper_band
        return buy_signal, sell_signal