import pandas as pd
import numpy as np

class BB:
    def __init__(self, prices, window=20, num_std_dev=2):
        self.prices = prices
        self.window = window
        self.num_std_dev = num_std_dev
        self.middle_band, self.upper_band, self.lower_band = self.calculate_bands()
    
    def calculate_bands(self):
        middle_band = self.prices['Close'].rolling(self.window).mean()
        std_dev = self.prices['Close'].rolling(self.window).std()
        upper_band = middle_band + (std_dev * self.num_std_dev)
        lower_band = middle_band - (std_dev * self.num_std_dev)
        return middle_band, upper_band, lower_band

    def cross_signal(self):
        buy_signal = (self.prices['Close'] > self.lower_band).shift(1) & (self.prices['Close'] <= self.lower_band)
        sell_signal = (self.prices['Close'] < self.lower_band).shift(1) | (self.prices['Close'] > self.upper_band)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.prices['Close'] < self.lower_band
        sell_signal = self.prices['Close'] > self.upper_band
        return buy_signal, sell_signal
