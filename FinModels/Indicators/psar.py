import pandas as pd
import numpy as np

class PSAR:
    """
    Parabolic SAR (Stop and Reverse) is a trend-following indicator that provides potential entry and exit points.
    It places dots above or below the price, depending on the trend direction.
    """
    def __init__(self, prices, af_increment=0.02, af_max=0.2):
        self.prices = prices
        self.af_increment = af_increment
        self.af_max = af_max
        self.psar = self.calculate_psar()
    
    def calculate_psar(self):
        af = self.af_increment
        psar = self.prices['Low'][0]
        ep = self.prices['High'][0]
        uptrend = True
        psar_series = [psar]

        for i in range(1, len(self.prices)):
            if uptrend:
                psar = psar + af * (ep - psar)
                if self.prices['High'][i] > ep:
                    ep = self.prices['High'][i]
                    af = min(af + self.af_increment, self.af_max)
                if self.prices['Low'][i] < psar:
                    uptrend = False
                    psar = ep
                    ep = self.prices['Low'][i]
                    af = self.af_increment
            else:
                psar = psar + af * (ep - psar)
                if self.prices['Low'][i] < ep:
                    ep = self.prices['Low'][i]
                    af = min(af + self.af_increment, self.af_max)
                if self.prices['High'][i] > psar:
                    uptrend = True
                    psar = ep
                    ep = self.prices['High'][i]
                    af = self.af_increment
            psar_series.append(psar)

        return pd.Series(psar_series, index=self.prices.index)
    
    def aux_signal(self):
        buy_signal = self.prices['Close'] > self.psar
        sell_signal = self.prices['Close'] < self.psar
        return buy_signal, sell_signal