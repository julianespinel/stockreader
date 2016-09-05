import unittest
import pymongo
import test.factories as factories

from src.stocks import mongo
from src.infrastructure import json

class MongoTest(unittest.TestCase):

    def setUp(self):
        dbHost = "localhost"
        dbPort = 27017
        testDBName = "test_stockreader_db"
        self.mongo = mongo.Mongo(dbHost, dbPort, testDBName)

    def tearDown(self):
        testDBName = "test_stockreader_db"
        mongoClient = pymongo.MongoClient()
        mongoClient.drop_database(testDBName)

    def testSaveStockList_OK(self):
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(0, stockCount)
        stocks = factories.get_stock_list()
        self.mongo.save_stock_list(stocks)
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(len(stocks), stockCount)

    def testSaveStockList_NOK_duplicateStock(self):
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(0, stockCount)
        stocks = factories.get_stock_list()
        stocks.append(stocks[0])
        self.mongo.save_stock_list(stocks)
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(len(stocks) - 1, stockCount)

    def testStockExists_OK(self):
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(0, stockCount)
        stocks = factories.get_stock_list()
        self.mongo.save_stock_list(stocks)
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(len(stocks), stockCount)
        self.assertTrue(self.mongo.stock_exists("FB"))

    def testStockExists_NOK_emptyStockList(self):
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(0, stockCount)
        stocks = []
        self.mongo.save_stock_list(stocks)
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(len(stocks), stockCount)
        self.assertFalse(self.mongo.stock_exists("FB"))

    def testGetStockByQuote_OK(self):
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(0, stockCount)
        stocks = factories.get_stock_list()
        self.mongo.save_stock_list(stocks)
        stockCount = len(self.mongo.read_stocks_from_stockList())
        self.assertEquals(len(stocks), stockCount)
        expectedStock = stocks[0]
        stockByQuote = self.mongo.get_stock_by_quote(expectedStock["symbol"])
        self.assertEquals(expectedStock, stockByQuote)

    def testSaveStockHistoricalData_OK(self):
        quote = "BAC"
        historicalStockEntries = len(self.mongo.get_stock_historical_data(quote))
        self.assertEquals(0, historicalStockEntries)
        stockHistoricalDataArray = factories.get_stock_historical_data_array()
        stockHistoricalDataArray = json.json_keys_to_lower_and_snake_case(stockHistoricalDataArray)
        self.mongo.save_stock_historical_data(quote, stockHistoricalDataArray)
        historicalStockEntries = len(self.mongo.get_stock_historical_data(quote))
        self.assertEquals(len(stockHistoricalDataArray), historicalStockEntries)

    def testUpsertStockCurrentData_OK(self):
        quote = "BAC"
        currentData = self.mongo.get_stock_current_data(quote)
        self.assertIsNone(currentData)
        stockCurrentData = factories.get_stock_current_data()
        stockCurrentData = json.json_keys_to_lower_and_snake_case(stockCurrentData)
        self.mongo.upsert_stock_current_data(quote, stockCurrentData)
        currentData = self.mongo.get_stock_current_data(quote)
        currentData.pop("_id") # Remove MongoDB generated ID to match with stockCurrentData
        self.assertEquals(stockCurrentData, currentData)
