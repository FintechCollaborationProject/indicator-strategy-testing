import pandas as pd
import numpy as np

class DPO:
    def __init__(self, prices, window=10):
        self.prices = prices
        self.window = window
        self.dpo = self.calculate_dpo()
    
    def calculate_dpo(self):
        n = int((self.window + 1) / 2)
        ma = self.prices['Close'].rolling(window=n).mean()
        dpo = self.prices['Close'] - ma.shift(n)
        return dpo
    
    def aux_signal(self):
        buy_signal = self.dpo > 0
        sell_signal = self.dpo < 0
        return buy_signal, sell_signal
