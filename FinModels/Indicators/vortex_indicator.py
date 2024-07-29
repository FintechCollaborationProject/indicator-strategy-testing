import pandas as pd
import numpy as np

class VI:
    def __init__(self, prices, window=14):
        self.prices = prices
        self.window = window
        self.vi_plus, self.vi_minus = self.calculate_vi()

    def calculate_vi(self):
        high_low = self.prices['High'] - self.prices['Low']
        high_close_prev = np.abs(self.prices['High'] - self.prices['Close'].shift(1))
        low_close_prev = np.abs(self.prices['Low'] - self.prices['Close'].shift(1))

        true_range = pd.DataFrame([high_low, high_close_prev, low_close_prev]).max()

        vm_plus = np.abs(self.prices['High'] - self.prices['Low'].shift(1))
        vm_minus = np.abs(self.prices['Low'] - self.prices['High'].shift(1))

        sum_tr = true_range.rolling(window=self.window).sum()
        sum_vm_plus = vm_plus.rolling(window=self.window).sum()
        sum_vm_minus = vm_minus.rolling(window=self.window).sum()

        vi_plus = sum_vm_plus / sum_tr
        vi_minus = sum_vm_minus / sum_tr

        return vi_plus, vi_minus

    def cross_signal(self):
        buy_signal = (self.vi_plus > self.vi_minus) & (self.vi_plus.shift(1) <= self.vi_minus.shift(1))
        sell_signal = (self.vi_plus < self.vi_minus) & (self.vi_plus.shift(1) >= self.vi_minus.shift(1))
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.vi_plus > self.vi_minus
        sell_signal = self.vi_plus < self.vi_minus
        return buy_signal, sell_signal
