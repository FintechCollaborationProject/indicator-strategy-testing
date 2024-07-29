import pandas as pd
import numpy as np

class CombinedIndicatorStrategy:
    def __init__(self, indicators):
        """
        Initialize the CombinedIndicatorStrategy with a list of indicators.

        :param indicators: A list of indicator objects.
        """
        self.indicators = indicators
        self.validate_indicators()
    
    def validate_indicators(self):
        """
        Validate the indicators to ensure they meet the expected types and attributes.
        """
        if not self.indicators:
            raise ValueError("No indicators provided. At least one indicator is required.")

        # Check the first indicator for the 'cross_signal' method
        if not hasattr(self.indicators[0], 'cross_signal') or not callable(getattr(self.indicators[0], 'cross_signal')):
            raise ValueError("The first indicator must have a 'cross_signal' method.")

        # Check subsequent indicators for the 'aux_signal' method
        for i, indicator in enumerate(self.indicators[1:], start=1):
            if not hasattr(indicator, 'aux_signal') or not callable(getattr(indicator, 'aux_signal')):
                raise ValueError(f"The indicator at position {i + 1} must have an 'aux_signal' method.")
    
    def generate_signals(self):
        """
        Generate buy and sell signals by combining signals from the provided indicators.

        :return: Two Series objects representing combined buy and sell signals.
        """
        buy_signals = []
        sell_signals = []

        # Process the first indicator (CROSS signal)
        cross_buy, cross_sell = self.indicators[0].cross_signal()
        buy_signals.append(cross_buy)
        sell_signals.append(cross_sell)

        # Process subsequent indicators (AUX signals)
        for indicator in self.indicators[1:]:
            aux_buy, aux_sell = indicator.aux_signal()
            buy_signals.append(aux_buy)
            sell_signals.append(aux_sell)

        # Combine the signals using 'any' to generate a signal if any of the conditions are met
        combined_buy_signal = pd.concat(buy_signals, axis=1).any(axis=1)
        combined_sell_signal = pd.concat(sell_signals, axis=1).any(axis=1)

        return combined_buy_signal, combined_sell_signal
