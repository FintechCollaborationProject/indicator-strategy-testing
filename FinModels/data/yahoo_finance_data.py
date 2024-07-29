import yfinance as yf

class YahooFinanceData:
    def __init__(self, ticker, start_date, end_date, interval='1d'):
        """
        Initializes the YahooFinanceData object with the ticker symbol, date range, and data interval.

        :param ticker: The stock ticker symbol (e.g., 'AAPL').
        :param start_date: The start date for fetching historical data (format: 'YYYY-MM-DD').
        :param end_date: The end date for fetching historical data (format: 'YYYY-MM-DD').
        :param interval: The interval between data points (default is '1d' for daily data).
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = None
    
    def fetch_data(self):
        """
        Fetches historical data from Yahoo Finance based on the initialized parameters.
        """
        try:
            self.data = yf.download(
                self.ticker, 
                start=self.start_date, 
                end=self.end_date, 
                interval=self.interval
            )
            print(f"Data fetched successfully for {self.ticker}")
        except Exception as e:
            print(f"An error occurred while fetching data: {e}")
    
    def get_data(self):
        """
        Returns the fetched data as a pandas DataFrame.

        :return: A pandas DataFrame containing the historical data.
        """
        if self.data is not None:
            return self.data
        else:
            print("Data not available. Please fetch data first.")
            return None
