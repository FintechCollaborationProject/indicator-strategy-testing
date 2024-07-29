class KeltnerChannel:
    def __init__(self, prices, window=20, multiplier=2):
        self.prices = prices
        self.window = window
        self.multiplier = multiplier
        self.middle_band, self.upper_band, self.lower_band = self.calculate_bands()
    
    def calculate_bands(self):
        middle_band = self.prices.ewm(span=self.window, adjust=False).mean()
        atr = self.prices.rolling(window=self.window).apply(lambda x: np.max(x) - np.min(x), raw=True)
        upper_band = middle_band + (atr * self.multiplier)
        lower_band = middle_band - (atr * self.multiplier)
        return middle_band, upper_band, lower_band

    def cross_signal(self):
        buy_signal = (self.prices > self.lower_band).shift(1) & (self.prices <= self.lower_band)
        sell_signal = (self.prices < self.lower_band) | (self.prices > self.upper_band)
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.prices < self.lower_band
        sell_signal = self.prices > self.upper_band
        return buy_signal, sell_signal