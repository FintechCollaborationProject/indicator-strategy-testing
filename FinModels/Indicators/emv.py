import pandas as pd
import numpy as np
class EMV:
    def __init__(self, prices, window=9):
        self.prices = prices
        self.window = window
        self.emv, self.emv_ma = self.calculate_emv()
    
    def calculate_emv(self):
        midpoint_move = ((self.prices['High'] + self.prices['Low']) / 2) - ((self.prices['High'].shift(1) + self.prices['Low'].shift(1)) / 2)
        box_ratio = (self.prices['Volume'] / 10000) / (self.prices['High'] - self.prices['Low'])
        emv = midpoint_move / box_ratio
        emv_ma = emv.rolling(self.window).mean()
        return emv, emv_ma
    
    def cross_signal(self):
        buy_signal = (self.emv > self.emv_ma).shift(1) & (self.emv <= self.emv_ma)
        sell_signal = (self.emv < self.emv_ma).shift(1) & (self.emv >= self.emv_ma)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.emv > 0
        sell_signal = self.emv < 0
        return buy_signal, sell_signal