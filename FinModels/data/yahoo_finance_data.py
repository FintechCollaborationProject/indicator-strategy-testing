import yfinance as yf
import pandas as pd

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

        This method attempts to download the data and stores it in the `data` attribute. 
        It also handles potential errors during the fetch process.
        """
        try:
            self.data = yf.download(
                self.ticker, 
                start=self.start_date, 
                end=self.end_date, 
                interval=self.interval
            )
            if not self.data.empty:
                print(f"Data fetched successfully for {self.ticker}")
            else:
                print(f"No data found for {self.ticker} in the given date range.")
        except Exception as e:
            print(f"An error occurred while fetching data for {self.ticker}: {e}")
    
    def get_data(self):
        """
        Returns the fetched data as a pandas DataFrame.

        :return: A pandas DataFrame containing the historical data or None if data has not been fetched.
        """
        if self.data is not None and not self.data.empty:
            return self.data
        else:
            print("Data not available. Please fetch data first.")
            return None