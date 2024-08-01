import pandas as pd
import numpy as np

class MFI:
    def __init__(self, prices, n1=14, n2=9):
        self.prices = prices
        self.n1 = n1
        self.n2 = n2
        self.mfi, self.mfi_ma = self.calculate_mfi()
    
    def calculate_mfi(self):
        # Calculate typical price (TP)
        tp = (self.prices['High'] + self.prices['Low'] + self.prices['Close']) / 3
        
        # Calculate money flow
        money_flow = tp * self.prices['Volume']
        
        # Calculate positive and negative money flow
        positive_flow = money_flow.where(tp > tp.shift(1), 0).rolling(window=self.n1).sum()
        negative_flow = money_flow.where(tp < tp.shift(1), 0).rolling(window=self.n1).sum()
        
        # Calculate money ratio
        money_ratio = positive_flow / negative_flow
        
        # Calculate MFI
        mfi = 100 - (100 / (1 + money_ratio))
        
        # Calculate MFIMA
        mfi_ma = mfi.rolling(window=self.n2).mean()
        
        return mfi, mfi_ma
    
    def cross_signal(self):
        # Generate buy/sell signals based on the MFI crossing above/below MFIMA
        buy_signal = (self.mfi > self.mfi_ma).shift(1) & (self.mfi <= self.mfi_ma)
        sell_signal = (self.mfi < self.mfi_ma).shift(1) & (self.mfi >= self.mfi_ma)
        return buy_signal, sell_signal

    def aux_signal(self):
        # Generate buy/sell signals based on MFI being below 20 or above 80
        buy_signal = self.mfi < 20
        sell_signal = self.mfi > 80
        return buy_signal, sell_signal
