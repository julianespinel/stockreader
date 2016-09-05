import unittest

from src.stocks import read


class ReadTest(unittest.TestCase):

    def setUp(self):
        self.read = read.Read()

    def test_read_stocks_from_file_OK(self):
        file_path = "resources/NYSE-Volume-Percentage-Movers-2016-03-21.csv"
        stock_market = "nyse"
        stocks = self.read.read_stocks_from_file(file_path, stock_market)
        self.assertIsNot(0, len(stocks))
        stock = stocks[0]
        # Check stock structure
        self.assertIsNotNone(stock["name"])
        self.assertIsNotNone(stock["symbol"])
        self.assertIsNotNone(stock["stockMarket"])

    def test_read_stocks_from_multiple_files_OK(self):
        file_path_list = [
            "resources/NYSE-Volume-Percentage-Movers-2016-03-21.csv",
            "resources/NYSE-Most-Active-Stocks-2016-03-21.csv",
            "resources/NYSE-Biggest-Percentage-Gainers-2016-03-21.csv",
            "resources/NYSE-Biggest-Percentage-Decliners-2016-03-21.csv"
        ]
        stock_market = "nyse"
        stocks = self.read.read_stocks_from_multiple_files(file_path_list, stock_market)
        self.assertIsNot(0, len(stocks))
        stock = stocks[0]
        # Check stock structure
        self.assertIsNotNone(stock["name"])
        self.assertIsNotNone(stock["symbol"])
        self.assertIsNotNone(stock["stockMarket"])
