import itertools

class TradingIndicatorCombinations:
    CROSS_AUX_INDICATORS = [
        "BB", "DEMA", "EMA", "EMV", "KC", "KDJ", "MA", "MACD", "MFI", 
        "REX", "RMA", "TEMA", "TRIX", "UO", "VI"
    ]
    AUX_INDICATORS = [
        "ADI", "ADX", "CCI", "DPO", "MAE", "MOM", "OBV", "OSC", 
        "PSAR", "RSI", "WPR"
    ]
    ALL_INDICATORS = CROSS_AUX_INDICATORS + AUX_INDICATORS

    def __init__(self, indicators_to_use):
        self.indicators_to_use = indicators_to_use

    def generate_combinations(self):
        if self.indicators_to_use == ["ALL"]:
            first_position = self.CROSS_AUX_INDICATORS  # Ensure first indicator is from CROSS_AUX_INDICATORS
            second_position = self.ALL_INDICATORS + [None]
            third_position = self.ALL_INDICATORS + [None]
        else:
            first_position = self._get_indicators_by_category(self.indicators_to_use[0])
            second_position = self._get_indicators_by_category(self.indicators_to_use[1]) + [None]
            third_position = self._get_indicators_by_category(self.indicators_to_use[2]) + [None]

        # Generate combinations with up to 3 indicators
        combinations = []
        combinations.extend(self._generate_single_combinations(first_position))
        combinations.extend(self._generate_double_combinations(first_position, second_position))
        combinations.extend(self._generate_triple_combinations(first_position, second_position, third_position))

        # Ensure that no indicator appears more than twice in a combination
        valid_combinations = [comb for comb in combinations if self._validate_combination(comb)]

        return valid_combinations

    def _get_indicators_by_category(self, category):
        if category == "none":
            return [None]
        elif category == "AUX":
            return self.AUX_INDICATORS
        elif category == "Cross & AUX":
            return self.CROSS_AUX_INDICATORS
        else:
            raise ValueError("Invalid category specified")

    def _generate_single_combinations(self, first_position):
        return [[ind] for ind in first_position]

    def _generate_double_combinations(self, first_position, second_position):
        return [[fp, sp] for fp in first_position for sp in second_position if sp is not None]

    def _generate_triple_combinations(self, first_position, second_position, third_position):
        return [[fp, sp, tp] for fp in first_position for sp in second_position for tp in third_position if sp is not None and tp is not None]

    def _validate_combination(self, combination):
        indicator_counts = {ind: combination.count(ind) for ind in combination}
        return all(count <= 2 for count in indicator_counts.values())

# # Example usage
# if __name__ == "__main__":
#     indicators_to_use = ["ALL"]
#     tic = TradingIndicatorCombinations(indicators_to_use)
#     combinations = tic.generate_combinations()

#     print("Generated Combinations:")
#     for combo in combinations:
#         print(combo)
