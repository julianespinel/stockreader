import unittest
from unittest.mock import Mock
from src.domain import Domain
from src.download import Download
from src.mongo import Mongo

class DomainTest(unittest.TestCase):

    def setUp(self):
        self.mongoMock = Mongo()
        self.downloadMock = Download()
        self.domain = Domain(self.mongoMock, self.downloadMock)

    def testDownloadAndSaveStockCurrentData(self):
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        stockCurrentData = {
            "symbol" : "BAC",
            "DaysLow" : "13.780",
            "StockExchange" : "NYQ",
            "DaysRange" : "13.780 - 13.940",
            "Volume" : "3255146",
            "LastTradePriceOnly" : "13.925",
            "YearHigh" : "18.480",
            "MarketCapitalization" : "146.44B",
            "Name" : "Bank of America Corporation Com",
            "AverageDailyVolume" : "136399008",
            "Change" : "+0.135",
            "DaysHigh" : "13.940",
            "Symbol" : "BAC",
            "YearLow" : "10.990"
        }
        self.downloadMock.getStockCurrentData = Mock(return_value=stockCurrentData)
        self.mongoMock.upsertStockCurrentData = Mock()
        self.domain.downloadAndSaveStockCurrentData(stock)
        self.downloadMock.getStockCurrentData.assert_called_once_with(quote)
        self.mongoMock.upsertStockCurrentData.assert_called_once_with(quote, stockCurrentData)

if __name__ == "main":
    unittest.main()
