import numpy as np

class TGR:
    def __init__(self, returns):
        """
        Initialize the TGR object.

        :param returns: List or array-like of annual return rates as percentages (e.g., 5.0 for 5%).
        """
        if not isinstance(returns, (list, np.ndarray)) or len(returns) == 0:
            raise ValueError("Returns must be a non-empty list or array-like of numbers.")
        
        self.returns = np.array(returns, dtype=float)

    def calculate(self):
        """
        Calculate the Total Growth Rate (TGR).

        :return: TGR as a percentage.
        """
        total_growth = np.prod(1 + self.returns / 100) - 1
        return total_growth * 100  # Convert to percentage

# Example usage:
#tgr_calculator = TGR([10, -5, 15])
#print(tgr_calculator.calculate())  # Output will be the TGR as a percentage

