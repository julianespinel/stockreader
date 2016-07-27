import unittest
from unittest.mock import Mock
from datetime import date, timedelta

from .context import src
from src import mongo
from src import download
from src import domain

class DomainTest(unittest.TestCase):

    def setUp(self):
        self.mongoMock = mongo.Mongo()
        self.downloadMock = download.Download()
        self.domain = domain.Domain(self.mongoMock, self.downloadMock)

    def testDownloadAndSaveStockCurrentData_OK(self):
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

    def testDownloadAndSaveStockCurrentData_NOK_emptyStockCurrentData(self):
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        stockCurrentData = None
        self.downloadMock.getStockCurrentData = Mock(return_value=stockCurrentData)
        self.mongoMock.upsertStockCurrentData = Mock()
        self.domain.downloadAndSaveStockCurrentData(stock)
        self.downloadMock.getStockCurrentData.assert_called_once_with(quote)
        self.mongoMock.upsertStockCurrentData.assert_called_once_with(quote, stockCurrentData)

    def testDownloadAndSaveStockDataDaysFromToday_OK(self):
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        daysFromToday = 3
        stockHistoricalDataArray = [
            {
                "Adj_Close": "13.79",
                "Date": "2016-03-18",
                "Close": "13.79",
                "Volume": "145037500",
                "Open": "13.68",
                "Low": "13.55",
                "High": "13.88",
                "Symbol": "BAC"
            },
            {
                "Adj_Close": "13.40",
                "Date": "2016-03-17",
                "Close": "13.40",
                "Volume": "121732700",
                "Open": "13.22",
                "Low": "13.05",
                "High": "13.48",
                "Symbol": "BAC"
            },
            {
                "Adj_Close": "13.31",
                "Date": "2016-03-16",
                "Close": "13.31",
                "Volume": "148489100",
                "Open": "13.51",
                "Low": "13.09",
                "High": "13.81",
                "Symbol": "BAC"
            }
        ]
        self.downloadMock.getStockHistoricalData = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.saveStockHistoricalData = Mock()
        self.domain.downloadAndSaveStockDataDaysFromToday(stock, daysFromToday)
        today = date.today()
        initialDate = today - timedelta(days=daysFromToday)
        self.downloadMock.getStockHistoricalData.assert_called_once_with(initialDate, today, quote)
        self.mongoMock.saveStockHistoricalData.assert_called_once_with(quote, stockHistoricalDataArray)

    def testDownloadAndSaveStockDataDaysFromToday_NOK_emptyStockHistoricalDataArray(self):
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        daysFromToday = 3
        stockHistoricalDataArray = []
        self.downloadMock.getStockHistoricalData = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.saveStockHistoricalData = Mock()
        self.domain.downloadAndSaveStockDataDaysFromToday(stock, daysFromToday)
        today = date.today()
        initialDate = today - timedelta(days=daysFromToday)
        self.downloadMock.getStockHistoricalData.assert_called_once_with(initialDate, today, quote)
        self.mongoMock.saveStockHistoricalData.assert_called_once_with(quote, stockHistoricalDataArray)

    def testDownloadAndSaveStockHistoricalData_OK(self):
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        stockHistoricalDataArray = [
            {
                "Adj_Close": "13.79",
                "Date": "2016-03-18",
                "Close": "13.79",
                "Volume": "145037500",
                "Open": "13.68",
                "Low": "13.55",
                "High": "13.88",
                "Symbol": "BAC"
            },
            {
                "Adj_Close": "13.40",
                "Date": "2016-03-17",
                "Close": "13.40",
                "Volume": "121732700",
                "Open": "13.22",
                "Low": "13.05",
                "High": "13.48",
                "Symbol": "BAC"
            },
            {
                "Adj_Close": "13.31",
                "Date": "2016-03-16",
                "Close": "13.31",
                "Volume": "148489100",
                "Open": "13.51",
                "Low": "13.09",
                "High": "13.81",
                "Symbol": "BAC"
            }
        ]
        self.downloadMock.getStockHistoricalData = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.saveStockHistoricalData = Mock()
        self.domain.downloadAndSaveStockHistoricalData(stock)
        self.assertTrue(self.downloadMock.getStockHistoricalData.call_count == self.domain.YEARS_AGO)
        self.mongoMock.saveStockHistoricalData.assert_called_with(quote, stockHistoricalDataArray)
        self.assertTrue(self.mongoMock.saveStockHistoricalData.call_count == self.domain.YEARS_AGO)

    def testDownloadAndSaveStockHistoricalData_NOK_emptyStockHistoricalDataArray(self):
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        stockHistoricalDataArray = []
        self.downloadMock.getStockHistoricalData = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.saveStockHistoricalData = Mock()
        self.domain.downloadAndSaveStockHistoricalData(stock)
        self.assertTrue(self.downloadMock.getStockHistoricalData.call_count == self.domain.YEARS_AGO)
        self.mongoMock.saveStockHistoricalData.assert_called_with(quote, stockHistoricalDataArray)
        self.assertTrue(self.mongoMock.saveStockHistoricalData.call_count == self.domain.YEARS_AGO)

if __name__ == "main":
    unittest.main()
