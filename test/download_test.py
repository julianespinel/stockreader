import datetime
import unittest

from src.stocks import download


class DownloadTest(unittest.TestCase):

    def setUp(self):
        self.download = download.Download()

    def testGetStockHistoricalData_OK(self):
        initialDate = datetime.date(2016, 7, 1)
        finalDate = datetime.date(2016, 7, 30)
        quote = "BAC"
        stockHistoricalDataArray = self.download.getStockHistoricalData(initialDate, finalDate, quote)
        self.assertIsNot(0, len(stockHistoricalDataArray))
        historicalData = stockHistoricalDataArray[0]
        # Check one element structure
        self.assertIsNotNone(historicalData["Symbol"])
        self.assertIsNotNone(historicalData["Date"])
        self.assertIsNotNone(historicalData["Open"])
        self.assertIsNotNone(historicalData["High"])
        self.assertIsNotNone(historicalData["Low"])
        self.assertIsNotNone(historicalData["Close"])
        self.assertIsNotNone(historicalData["Volume"])
        self.assertIsNotNone(historicalData["Adj_Close"])

    def testGetStockCurrentData_OK(self):
        quote = "BAC"
        stockCurrentData = self.download.getStockCurrentData(quote)
        self.assertIsNotNone(stockCurrentData)
        # Check current data structure
        self.assertIsNotNone(stockCurrentData["symbol"])
        self.assertIsNotNone(stockCurrentData["AverageDailyVolume"])
        self.assertIsNotNone(stockCurrentData["Change"])
        self.assertIsNotNone(stockCurrentData["DaysLow"])
        self.assertIsNotNone(stockCurrentData["DaysHigh"])
        self.assertIsNotNone(stockCurrentData["YearLow"])
        self.assertIsNotNone(stockCurrentData["YearHigh"])
        self.assertIsNotNone(stockCurrentData["MarketCapitalization"])
        self.assertIsNotNone(stockCurrentData["LastTradePriceOnly"])
        self.assertIsNotNone(stockCurrentData["DaysRange"])
        self.assertIsNotNone(stockCurrentData["Name"])
        self.assertIsNotNone(stockCurrentData["Symbol"])
        self.assertIsNotNone(stockCurrentData["Volume"])
        self.assertIsNotNone(stockCurrentData["StockExchange"])
