import numpy as np

class CAGR:
    def __init__(self, returns, num_years):
        """
        Initialize the CAGR object.

        :param returns: List or array-like of annual return rates as percentages (e.g., 5.0 for 5%).
        """
        # Validate the returns input
        if not isinstance(returns, (list, np.ndarray)) or len(returns) == 0:
            raise ValueError("Returns must be a non-empty list or array-like of numbers.")
        
        # Ensure all elements are numeric
        self.returns = np.array(returns, dtype=float)
        self.num_years = num_years
    
    def calculate(self):
        """
        Calculate the Compound Annual Growth Rate (CAGR).

        :return: CAGR as a percentage.
        """
        if self.num_years == 0:
            raise ValueError("Number of years must be greater than zero.")
        
        # Calculate the final value after the period
        final_value = np.prod(1 + self.returns / 100)
        
        # Calculate CAGR
        cagr = (final_value ** (1 / self.num_years) - 1) * 100  # Convert to percentage
        return cagr

# Example usage:
#cagr_calculator = CAGR([10, -5, 15])
#print(cagr_calculator.calculate())  # Output will be the CAGR as a percentage

