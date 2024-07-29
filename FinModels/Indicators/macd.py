class MACD:
    def __init__(self, prices, short_window=12, long_window=26, signal_window=9):
        self.prices = prices
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.macd_line, self.signal_line, self.histogram = self.calculate_macd()
    
    def calculate_macd(self):
        short_ema = self.prices.ewm(span=self.short_window, adjust=False).mean()
        long_ema = self.prices.ewm(span=self.long_window, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=self.signal_window, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    def cross_signal(self):
        buy_signal = (self.macd_line > self.signal_line) & (self.macd_line.shift(1) <= self.signal_line.shift(1))
        sell_signal = (self.macd_line < self.signal_line) & (self.macd_line.shift(1) >= self.signal_line.shift(1))
        return buy_signal, sell_signal

    def aux_signal(self):
        buy_signal = self.macd_line > self.signal_line
        sell_signal = self.macd_line < self.signal_line
        return buy_signal, sell_signal
