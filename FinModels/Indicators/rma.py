import pandas as pd
import numpy as np

class RMA:
    def __init__(self, prices, short_window=10, long_window=30):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.short_rma, self.long_rma = self.calculate_rma()
    
    def calculate_rma(self):
        # RMA is essentially an EMA
        short_rma = self.prices['Close'].ewm(span=self.short_window, adjust=False).mean()
        long_rma = self.prices['Close'].ewm(span=self.long_window, adjust=False).mean()
        return short_rma, long_rma
    
    def cross_signal(self):
        buy_signal = (self.short_rma > self.long_rma).shift(1) & (self.short_rma <= self.long_rma)
        sell_signal = (self.short_rma < self.long_rma).shift(1) & (self.short_rma >= self.long_rma)
        return buy_signal, sell_signal

    def aux_signal(self):
        long_entry_or_short_exit = self.short_rma > self.long_rma
        short_entry_or_long_exit = self.short_rma < self.long_rma
        return long_entry_or_short_exit, short_entry_or_long_exit
