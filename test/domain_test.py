import unittest
from unittest.mock import Mock
from datetime import date, timedelta

from .context import src
from src import domain

class DomainTest(unittest.TestCase):

    def setUp(self):
        self.mongoMock = Mock()
        self.downloadMock = Mock()
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

    def testDownloadAndSaveStockHistoricalData_OK(self):
        initialDate = date(2006, 9, 1)
        finalDate = date(2016, 9, 1)
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
        self.domain.downloadAndSaveStockHistoricalData(initialDate, finalDate, stock)
        self.downloadMock.getStockHistoricalData.assert_called_once_with(initialDate, finalDate, quote)
        self.mongoMock.saveStockHistoricalData.assert_called_once_with(quote, stockHistoricalDataArray)

    def testDownloadAndSaveStockHistoricalData_NOK_emptyStockHistoricalDataArray(self):
        initialDate = date(2006, 9, 1)
        finalDate = date(2016, 9, 1)
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        stockHistoricalDataArray = []
        self.downloadMock.getStockHistoricalData = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.saveStockHistoricalData = Mock()
        self.domain.downloadAndSaveStockHistoricalData(initialDate, finalDate, stock)
        self.downloadMock.getStockHistoricalData.assert_called_once_with(initialDate, finalDate, quote)
        self.mongoMock.saveStockHistoricalData.assert_called_once_with(quote, stockHistoricalDataArray)

    def testStockExists_OK(self):
        quote = "BAC"
        expectedResult = True
        self.mongoMock.stockExists = Mock(return_value=expectedResult)
        self.assertEqual(expectedResult, self.domain.stockExists(quote))
        self.mongoMock.stockExists.assert_called_once_with(quote)

    def testStockExists_NOK_stockDoesNotExists(self):
        quote = "BAC"
        expectedResult = False
        self.mongoMock.stockExists = Mock(return_value=expectedResult)
        self.assertEqual(expectedResult, self.domain.stockExists(quote))
        self.mongoMock.stockExists.assert_called_once_with(quote)

    def testGetStockList_OK(self):
        expectedStockList = [
            { "stockMarket" : "nyse", "name" : "Valspar", "quote" : "VAL" },
            { "stockMarket" : "nyse", "name" : "Trinseo", "quote" : "TSE" },
            { "stockMarket" : "nyse", "name" : "Celestica", "quote" : "CLS" }
        ]
        self.mongoMock.readStocksFromStockList = Mock(return_value=expectedStockList)
        stockList = self.domain.getStockList()
        self.assertEqual(len(expectedStockList), len(stockList))
        self.mongoMock.readStocksFromStockList.assert_called_once_with()

    def testGetStockList_NOK_emptyStockList(self):
        expectedStockList = []
        self.mongoMock.readStocksFromStockList = Mock(return_value=expectedStockList)
        stockList = self.domain.getStockList()
        self.assertEqual(len(expectedStockList), len(stockList))
        self.mongoMock.readStocksFromStockList.assert_called_once_with()

    def testAddStockToStockList_OK(self):
        stock = { "stockMarket" : "nyse", "name" : "Trinseo", "quote" : "TSE" }
        self.mongoMock.saveStockList = Mock()
        self.domain.addStockToStockList(stock)
        self.mongoMock.saveStockList.assert_called_once_with([stock])

if __name__ == "main":
    unittest.main()
