import pandas as pd
import numpy as np

class ReturnAnalysis:
    def __init__(self, returns, num_years):
        """
        Initialize ReturnAnalysis with annual returns.

        :param returns: A list or array-like structure containing annual returns.
        :raises ValueError: If returns are not a non-empty list or array-like of numbers.
        """
        if not isinstance(returns, (list, np.ndarray)) or len(returns) == 0:
            raise ValueError("Returns must be a non-empty list or array-like of numbers.")
        
        self.returns = np.array(returns, dtype=np.float64)
        self.num_years = num_years
        self.avg_return = np.mean(self.returns)
        self.std_deviation = np.std(self.returns)
        self.median_return = np.median(self.returns)
        self.percentile_25 = np.percentile(self.returns, 25)
        self.percentile_75 = np.percentile(self.returns, 75)
        self.min_return = np.min(self.returns)
        self.max_return = np.max(self.returns)

    def get_summary(self):
        """
        Generate a summary of the return analysis.

        :return: A dictionary containing the summary statistics.
        """
        return {
            "Number of Years": self.num_years,
            "Average Return Rate (%)": self.avg_return,
            "Median Return Rate (%)": self.median_return,
            "Standard Deviation (%)": self.std_deviation,
            "25th Percentile (%)": self.percentile_25,
            "75th Percentile (%)": self.percentile_75,
            "Minimum Return Rate (%)": self.min_return,
            "Maximum Return Rate (%)": self.max_return
        }

    def to_dataframe(self):
        """
        Convert the summary statistics to a pandas DataFrame.

        :return: DataFrame containing the summary statistics.
        """
        summary = self.get_summary()
        return pd.DataFrame([summary])

    def summary_as_string(self):
        """
        Get a string representation of the summary statistics.

        :return: A string containing the formatted summary statistics.
        """
        summary = self.get_summary()
        return '\n'.join(f"{key}: {value:.2f}" for key, value in summary.items())
