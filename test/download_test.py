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
        self.assertIsNotNone(historicalData["symbol"])
        self.assertIsNotNone(historicalData["date"])
        self.assertIsNotNone(historicalData["open"])
        self.assertIsNotNone(historicalData["high"])
        self.assertIsNotNone(historicalData["low"])
        self.assertIsNotNone(historicalData["close"])
        self.assertIsNotNone(historicalData["volume"])
        self.assertIsNotNone(historicalData["adj_close"])

    def testGetStockCurrentData_OK(self):
        quote = "BAC"
        stockCurrentData = self.download.getStockCurrentData(quote)
        self.assertIsNotNone(stockCurrentData)
        # Check current data structure
        self.assertIsNotNone(stockCurrentData["symbol"])
        self.assertIsNotNone(stockCurrentData["average_daily_volume"])
        self.assertIsNotNone(stockCurrentData["change"])
        self.assertIsNotNone(stockCurrentData["days_low"])
        self.assertIsNotNone(stockCurrentData["days_high"])
        self.assertIsNotNone(stockCurrentData["year_low"])
        self.assertIsNotNone(stockCurrentData["year_high"])
        self.assertIsNotNone(stockCurrentData["market_capitalization"])
        self.assertIsNotNone(stockCurrentData["last_trade_price_only"])
        self.assertIsNotNone(stockCurrentData["days_range"])
        self.assertIsNotNone(stockCurrentData["name"])
        self.assertIsNotNone(stockCurrentData["symbol"])
        self.assertIsNotNone(stockCurrentData["volume"])
        self.assertIsNotNone(stockCurrentData["stock_exchange"])
