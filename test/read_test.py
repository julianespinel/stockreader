import unittest

from .context import src
from src import read

class ReadTest(unittest.TestCase):

    def setUp(self):
        self.read = read.Read()

    def testReadStocksFromFile_OK(self):
        filePath = "resources/NYSE-Volume-Percentage-Movers-2016-03-21.csv"
        stockMarket = "nyse"
        stocks = self.read.readStocksFromFile(filePath, stockMarket)
        self.assertIsNot(0, len(stocks))
        stock = stocks[0]
        # Check stock structure
        self.assertIsNotNone(stock["name"])
        self.assertIsNotNone(stock["quote"])
        self.assertIsNotNone(stock["stockMarket"])

    def testReadStocksFromMultipleFiles(self):
        filePathList = [
            "resources/NYSE-Volume-Percentage-Movers-2016-03-21.csv",
            "resources/NYSE-Most-Active-Stocks-2016-03-21.csv",
            "resources/NYSE-Biggest-Percentage-Gainers-2016-03-21.csv",
            "resources/NYSE-Biggest-Percentage-Decliners-2016-03-21.csv"
        ]
        stockMarket = "nyse"
        stocks = self.read.readStocksFromMultipleFiles(filePathList, stockMarket)
        self.assertIsNot(0, len(stocks))
        stock = stocks[0]
        # Check stock structure
        self.assertIsNotNone(stock["name"])
        self.assertIsNotNone(stock["quote"])
        self.assertIsNotNone(stock["stockMarket"])
