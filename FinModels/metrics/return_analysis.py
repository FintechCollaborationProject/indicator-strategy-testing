import pandas as pd
import numpy as np

class ReturnAnalysis:
    def __init__(self, returns):
        """
        Initialize the ReturnAnalysis object.

        :param returns: List or array of annual return rates.
        """
        self.returns = returns
        self.num_years = len(returns)
        self.avg_return = np.mean(returns)
        self.std_deviation = np.std(returns)
        self.percentile_25 = np.percentile(returns, 25)
        self.percentile_75 = np.percentile(returns, 75)
        self.min_return = np.min(returns)
        self.max_return = np.max(returns)
    
    def get_summary(self):
        """
        Get a summary of the return analysis.

        :return: Dictionary containing summary statistics of returns.
        """
        return {
            "Number of Years": self.num_years,
            "Average Return Rate": self.avg_return,
            "Standard Deviation": self.std_deviation,
            "25th Percentile": self.percentile_25,
            "75th Percentile": self.percentile_75,
            "Minimum Return Rate": self.min_return,
            "Maximum Return Rate": self.max_return
        }
