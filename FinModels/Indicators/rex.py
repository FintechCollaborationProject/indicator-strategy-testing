import pandas as pd
import numpy as np

class REX:
    """
    REX (Rate of Change of Exponential Moving Average) measures the rate of change of EMA values.
    It helps identify the strength and direction of a trend.
    """
    def __init__(self, prices, short_window=2, long_window=10):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.rex = self.calculate_rex()
    
    def calculate_rex(self):
        ema_short = self.prices['Close'].ewm(span=self.short_window, adjust=False).mean()
        ema_long = self.prices['Close'].ewm(span=self.long_window, adjust=False).mean()
        rex = (ema_short - ema_long) / ema_long
        return rex
    
    def cross_signal(self):
        buy_signal = (self.rex > 0).shift(1) & (self.rex <= 0)
        sell_signal = (self.rex < 0).shift(1) & (self.rex >= 0)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.rex > 0
        sell_signal = self.rex < 0
        return buy_signal, sell_signal
