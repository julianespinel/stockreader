import datetime
import unittest

from src.stocks import download

@unittest.skip("skip integration test cases")
class DownloadTest(unittest.TestCase):

    def setUp(self):
        self.download = download.Download()

    def test_get_stock_historical_data_OK(self):
        initial_date = datetime.date(2016, 7, 1)
        final_date = datetime.date(2016, 7, 30)
        quote = "BAC"
        stock_historical_data_array = self.download.get_stock_historical_data(initial_date, final_date, quote)
        self.assertIsNot(0, len(stock_historical_data_array))
        historical_data = stock_historical_data_array[0]
        # Check one element structure
        self.assertIsNotNone(historical_data["symbol"])
        self.assertIsNotNone(historical_data["date"])
        self.assertIsNotNone(historical_data["open"])
        self.assertIsNotNone(historical_data["high"])
        self.assertIsNotNone(historical_data["low"])
        self.assertIsNotNone(historical_data["close"])
        self.assertIsNotNone(historical_data["volume"])
        self.assertIsNotNone(historical_data["adj_close"])

    def test_get_stock_current_data_OK(self):
        quote = "BAC"
        stock_current_data = self.download.get_stock_current_data(quote)
        self.assertIsNotNone(stock_current_data)
        # Check current data structure
        self.assertIsNotNone(stock_current_data["symbol"])
        self.assertIsNotNone(stock_current_data["average_daily_volume"])
        self.assertIsNotNone(stock_current_data["change"])
        self.assertIsNotNone(stock_current_data["days_low"])
        self.assertIsNotNone(stock_current_data["days_high"])
        self.assertIsNotNone(stock_current_data["year_low"])
        self.assertIsNotNone(stock_current_data["year_high"])
        self.assertIsNotNone(stock_current_data["market_capitalization"])
        self.assertIsNotNone(stock_current_data["last_trade_price_only"])
        self.assertIsNotNone(stock_current_data["days_range"])
        self.assertIsNotNone(stock_current_data["name"])
        self.assertIsNotNone(stock_current_data["symbol"])
        self.assertIsNotNone(stock_current_data["volume"])
        self.assertIsNotNone(stock_current_data["stock_exchange"])
