import pandas as pd
import numpy as np

class MAE:
    def __init__(self, prices, window=20, k=3):
        self.prices = prices
        self.window = window
        self.k = k
        self.upper, self.lower = self.calculate_mae()
    
    def calculate_mae(self):
        ma = self.prices['Close'].rolling(self.window).mean()
        upper = ma + ma * self.k / 100
        lower = ma - ma * self.k / 100
        return upper, lower
    
    def aux_signal(self):
        buy_signal = self.prices['Close'] < self.lower
        sell_signal = self.prices['Close'] > self.upper
        return buy_signal, sell_signal
