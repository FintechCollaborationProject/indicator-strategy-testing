import pandas as pd
import numpy as np

class CombinedIndicatorStrategy:
    def __init__(self, indicators):
        self.indicators = indicators
        self.validate_indicators()
    
    def validate_indicators(self):
        # Check the first indicator is a CROSS
        if not hasattr(self.indicators[0], 'cross_signal'):
            raise ValueError("The first indicator must be a CROSS type.")

        # Check the second and third indicators, if present, are AUX
        if len(self.indicators) > 1:
            if not hasattr(self.indicators[1], 'aux_signal'):
                raise ValueError("The second indicator must be an AUX type.")
        if len(self.indicators) > 2:
            if not hasattr(self.indicators[2], 'aux_signal'):
                raise ValueError("The third indicator must be an AUX type.")
    
    def generate_signals(self):
        # Initialize lists to hold buy and sell signals
        buy_signals = []
        sell_signals = []

        # Get the CROSS signals from the first indicator
        buy, sell = self.indicators[0].cross_signal()
        print(f"Cross signals - Buy: {buy.head()}, Sell: {sell.head()}")  # Debugging line
        buy_signals.append(buy)
        sell_signals.append(sell)

        # Get AUX signals from the second indicator, if present
        if len(self.indicators) > 1:
            buy, sell = self.indicators[1].aux_signal()
            print(f"AUX signals - Buy: {buy.head()}, Sell: {sell.head()}")  # Debugging line
            buy_signals.append(buy)
            sell_signals.append(sell)

        # Get AUX signals from the third indicator, if present
        if len(self.indicators) > 2:
            buy, sell = self.indicators[2].aux_signal()
            print(f"AUX signals - Buy: {buy.head()}, Sell: {sell.head()}")  # Debugging line
            buy_signals.append(buy)
            sell_signals.append(sell)

        # Combine the signals (consider changing 'all' to 'any' if you want to act on any signal)
        combined_buy_signal = pd.concat(buy_signals, axis=1).any(axis=1)
        combined_sell_signal = pd.concat(sell_signals, axis=1).any(axis=1)

        print(f"Combined Buy Signal: {combined_buy_signal.head()}")  # Debugging line
        print(f"Combined Sell Signal: {combined_sell_signal.head()}")  # Debugging line

        return combined_buy_signal, combined_sell_signal
