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
        stockCurrentData = factories.get_stock_current_data()
        self.downloadMock.get_stock_current_data = Mock(return_value=stockCurrentData)
        self.mongoMock.upsert_stock_current_data = Mock()
        self.domain.download_and_save_stock_current_data(stock)
        self.downloadMock.get_stock_current_data.assert_called_once_with(quote)
        self.mongoMock.upsert_stock_current_data.assert_called_once_with(quote, stockCurrentData)

    def testDownloadAndSaveStockCurrentData_NOK_emptyStockCurrentData(self):
        stock = factories.getStockData()
        quote = stock["symbol"]
        stockCurrentData = None
        self.downloadMock.get_stock_current_data = Mock(return_value=stockCurrentData)
        self.mongoMock.upsert_stock_current_data = Mock()
        self.domain.download_and_save_stock_current_data(stock)
        self.downloadMock.get_stock_current_data.assert_called_once_with(quote)
        self.mongoMock.upsert_stock_current_data.assert_called_once_with(quote, stockCurrentData)

    def testDownloadAndSaveStockHistoricalData_OK(self):
        initialDate = date(2006, 9, 1)
        finalDate = date(2016, 9, 1)
        stock = factories.getStockData()
        quote = stock["symbol"]
        stockHistoricalDataArray = factories.getStockHistoricalDataArray()
        self.downloadMock.get_stock_historical_data = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.save_stock_historical_data = Mock()
        self.domain.download_and_save_stock_historical_data(initialDate, finalDate, stock)
        self.downloadMock.get_stock_historical_data.assert_called_once_with(initialDate, finalDate, quote)
        self.mongoMock.save_stock_historical_data.assert_called_once_with(quote, stockHistoricalDataArray)

    def testDownloadAndSaveStockHistoricalData_NOK_emptyStockHistoricalDataArray(self):
        initialDate = date(2006, 9, 1)
        finalDate = date(2016, 9, 1)
        stock = factories.getStockData()
        quote = stock["symbol"]
        stockHistoricalDataArray = []
        self.downloadMock.get_stock_historical_data = Mock(return_value=stockHistoricalDataArray)
        self.mongoMock.save_stock_historical_data = Mock()
        self.domain.download_and_save_stock_historical_data(initialDate, finalDate, stock)
        self.downloadMock.get_stock_historical_data.assert_called_once_with(initialDate, finalDate, quote)
        self.mongoMock.save_stock_historical_data.assert_called_once_with(quote, stockHistoricalDataArray)

    def testStockExists_OK(self):
        quote = "BAC"
        expectedResult = True
        self.mongoMock.stock_exists = Mock(return_value=expectedResult)
        self.assertEqual(expectedResult, self.domain.stock_exists(quote))
        self.mongoMock.stock_exists.assert_called_once_with(quote)

    def testStockExists_NOK_stockDoesNotExists(self):
        quote = "BAC"
        expectedResult = False
        self.mongoMock.stock_exists = Mock(return_value=expectedResult)
        self.assertEqual(expectedResult, self.domain.stock_exists(quote))
        self.mongoMock.stock_exists.assert_called_once_with(quote)

    def testGetStockList_OK(self):
        expectedStockList = factories.getStockList()
        self.mongoMock.read_stocks_from_stock_list = Mock(return_value=expectedStockList)
        stockList = self.domain.get_stock_list()
        self.assertEqual(len(expectedStockList), len(stockList))
        self.mongoMock.read_stocks_from_stock_list.assert_called_once_with()

    def testGetStockList_NOK_emptyStockList(self):
        expectedStockList = []
        self.mongoMock.read_stocks_from_stock_list = Mock(return_value=expectedStockList)
        stockList = self.domain.get_stock_list()
        self.assertEqual(len(expectedStockList), len(stockList))
        self.mongoMock.read_stocks_from_stock_list.assert_called_once_with()

    def testAddStockToStockList_OK(self):
        stock = factories.getStockData()
        self.mongoMock.save_stock_list = Mock()
        self.domain.add_stock_to_stock_list(stock)
        self.mongoMock.save_stock_list.assert_called_once_with([stock])
