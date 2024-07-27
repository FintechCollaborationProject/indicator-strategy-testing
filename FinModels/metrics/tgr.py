import pandas as pd
import numpy as np

class TGR:
    def __init__(self, returns):
        """
        Initialize the TGR object.

        :param returns: List or array of annual return rates.
        """
        self.returns = returns
    
    def calculate(self):
        """
        Calculate the Total Growth Rate (TGR).

        :return: TGR as a percentage.
        """
        total_growth = np.prod([1 + r / 100 for r in self.returns]) - 1
        return total_growth * 100  # Convert to percentage
