import pandas as pd
import numpy as np

class ADI:
    def __init__(self, prices):
        self.prices = prices
        self.ad = self.calculate_ad()
    
    def calculate_ad(self):
        # Correct formula for MFM
        mfm = ((self.prices['Close'] - self.prices['Low']) - (self.prices['High'] - self.prices['Close'])) / (self.prices['High'] - self.prices['Low'])
        # Handle division by zero in MFM calculation
        mfm = mfm.replace([np.inf, -np.inf], 0).fillna(0)
        
        # MFV calculation
        mfv = mfm * self.prices['Volume']
        
        # Cumulative sum of MFV to get AD
        ad = mfv.cumsum()
        return ad
    
    def aux_signal(self):
        buy_signal = self.ad > 0
        sell_signal = self.ad < 0
        return buy_signal, sell_signal
