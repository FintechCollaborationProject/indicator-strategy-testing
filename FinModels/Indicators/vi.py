import pandas as pd
import numpy as np

class VI:
    def __init__(self, prices, window=14):
        self.prices = prices
        self.window = window
        self.tr, self.vm_plus, self.vm_minus = self.calculate_vm()
        self.vi_plus, self.vi_minus = self.calculate_vi()
    
    def calculate_vm(self):
        high = self.prices['High']
        low = self.prices['Low']
        close = self.prices['Close']
        tr = np.maximum(high, low.shift(1)) - np.minimum(low, close.shift(1))
        pd = high - low.shift(1)
        nd = high.shift(1) - low
        vm_plus = pd.rolling(self.window).sum() / tr.rolling(self.window).sum()
        vm_minus = nd.rolling(self.window).sum() / tr.rolling(self.window).sum()
        return tr, vm_plus, vm_minus
    
    def calculate_vi(self):
        vi_plus = self.vm_plus.rolling(self.window).mean()
        vi_minus = self.vm_minus.rolling(self.window).mean()
        return vi_plus, vi_minus
    
    def cross_signal(self):
        buy_signal = (self.vi_plus > self.vi_minus).shift(1) & (self.vi_plus <= self.vi_minus)
        sell_signal = (self.vi_plus < self.vi_minus).shift(1) & (self.vi_plus >= self.vi_minus)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.vi_plus > self.vi_minus
        sell_signal = self.vi_plus < self.vi_minus
        return buy_signal, sell_signal
