import pandas as pd
import numpy as np

class WPR:
    def __init__(self, prices, window=14):
        self.prices = prices
        self.window = window
        self.wpr = self.calculate_wpr()
    
    def calculate_wpr(self):
        highest_high = self.prices['High'].rolling(self.window).max()
        lowest_low = self.prices['Low'].rolling(self.window).min()
        wpr = (highest_high - self.prices['Close']) / (highest_high - lowest_low) * -100
        return wpr
    
    def aux_signal(self):
        buy_signal = self.wpr < -80
        sell_signal = self.wpr > -20
        return buy_signal, sell_signal
