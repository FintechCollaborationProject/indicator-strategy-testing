import pandas as pd
import numpy as np

class UO:
    def __init__(self, prices, n1=7, n2=14, n3=28, ns=3, nl=7):
        self.prices = prices
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.ns = ns
        self.nl = nl
        self.uo, self.uos, self.uol = self.calculate_uo()
    
    def calculate_uo(self):
        # Calculate Buying Pressure (BP)
        bp = self.prices['Close'] - np.minimum(self.prices['Low'], self.prices['Low'].shift(1))
        
        # Calculate True Range (TR)
        tr = np.maximum(self.prices['High'], self.prices['Low'].shift(1)) - np.minimum(self.prices['Low'], self.prices['Close'].shift(1))
        
        # Calculate averages for different periods
        avg_n1 = bp.rolling(self.n1).sum() / tr.rolling(self.n1).sum()
        avg_n2 = bp.rolling(self.n2).sum() / tr.rolling(self.n2).sum()
        avg_n3 = bp.rolling(self.n3).sum() / tr.rolling(self.n3).sum()
        
        # Calculate the Ultimate Oscillator (UO)
        uo = 100 * ((4 * avg_n1 + 2 * avg_n2 + avg_n3) / (4 + 2 + 1))
        
        # Signal line (short-term and long-term moving averages of UO)
        uos = uo.rolling(window=self.ns).mean()
        uol = uo.rolling(window=self.nl).mean()
        
        return uo, uos, uol
    
    def cross_signal(self):
        buy_signal = (self.uos > self.uol).shift(1) & (self.uos <= self.uol)
        sell_signal = (self.uos < self.uol).shift(1) & (self.uos >= self.uol)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.uo < 30
        sell_signal = self.uo > 70
        return buy_signal, sell_signal
