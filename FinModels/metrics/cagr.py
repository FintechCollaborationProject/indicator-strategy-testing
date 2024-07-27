import pandas as pd
import numpy as np

class CAGR:
    def __init__(self, returns):
        """
        Initialize the CAGR object.

        :param returns: List or array of annual return rates.
        """
        self.returns = returns
        self.num_years = len(returns)
    
    def calculate(self):
        """
        Calculate the Compound Annual Growth Rate (CAGR).

        :return: CAGR as a percentage.
        """
        final_value = np.prod([1 + r / 100 for r in self.returns])
        cagr = (final_value ** (1 / self.num_years) - 1) * 100  # Convert to percentage
        return cagr
