import unittest
import test.factories as factories

from datetime import date
from unittest.mock import Mock

from src.stocks import domain


class DomainTest(unittest.TestCase):

    def setUp(self):
        self.mongoMock = Mock()
        self.downloadMock = Mock()
        self.domain = domain.Domain(self.mongoMock, self.downloadMock)

    def testDownloadAndSaveStockCurrentData_OK(self):
        stock = factories.getStockData()
        quote = stock["symbol"]
        stockCurrentData = factories.getStockCurrentData()
        self.downloadMock.getStockCurrentData = Mock(return_value=stockCurrentData)
        self.mongoMock.upsertStockCurrentData = Mock()
        self.domain.downloadAndSaveStockCurrentData(stock)
        self.downloadMock.getStockCurrentData.assert_called_once_with(quote)
        self.mongoMock.upsertStockCurrentData.assert_called_once_with(quote, stockCurrentData)

    def testDownloadAndSaveStockCurrentData_NOK_emptyStockCurrentData(self):
        stock = factories.getStockData()
        quote = stock["symbol"]
        stockCurrentData = None
        self.downloadMock.getStockCurrentData = Mock(return_value=stockCurrentData)
        self.mongoMock.upsertStockCurrentData = Mock()
        self.domain.downloadAndSaveStockCurrentData(stock)
        self.downloadMock.getStockCurrentData.assert_called_once_with(quote)
        self.mongoMock.upsertStockCurrentData.assert_called_once_with(quote, stockCurrentData)

    def testDownloadAndSaveStockHistoricalData_OK(self):
        initialDate = date(2006, 9, 1)
        finalDate = date(2016, 9, 1)
        stock = factories.getStockData()
        quote = stock["symbol"]
        stockHistoricalDataArray = factories.getStockHistoricalDataArray()
        self.downloadMock.getStockHistoricalData = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.saveStockHistoricalData = Mock()
        self.domain.downloadAndSaveStockHistoricalData(initialDate, finalDate, stock)
        self.downloadMock.getStockHistoricalData.assert_called_once_with(initialDate, finalDate, quote)
        self.mongoMock.saveStockHistoricalData.assert_called_once_with(quote, stockHistoricalDataArray)

    def testDownloadAndSaveStockHistoricalData_NOK_emptyStockHistoricalDataArray(self):
        initialDate = date(2006, 9, 1)
        finalDate = date(2016, 9, 1)
        stock = factories.getStockData()
        quote = stock["symbol"]
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
        expectedStockList = factories.getStockList()
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
        stock = factories.getStockData()
        self.mongoMock.saveStockList = Mock()
        self.domain.addStockToStockList(stock)
        self.mongoMock.saveStockList.assert_called_once_with([stock])
