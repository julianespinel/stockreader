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
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = factories.getStockList()
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks), stockCount)

    def testSaveStockList_NOK_duplicateStock(self):
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = factories.getStockList()
        stocks.append(stocks[0])
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks) - 1, stockCount)

    def testStockExists_OK(self):
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = factories.getStockList()
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks), stockCount)
        self.assertTrue(self.mongo.stockExists("FB"))

    def testStockExists_NOK_emptyStockList(self):
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = []
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks), stockCount)
        self.assertFalse(self.mongo.stockExists("FB"))

    def testGetStockByQuote_OK(self):
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = factories.getStockList()
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks), stockCount)
        expectedStock = stocks[0]
        stockByQuote = self.mongo.getStockByQuote(expectedStock["symbol"])
        self.assertEquals(expectedStock, stockByQuote)

    def testSaveStockHistoricalData_OK(self):
        quote = "BAC"
        historicalStockEntries = len(self.mongo.getStockHistoricalData(quote))
        self.assertEquals(0, historicalStockEntries)
        stockHistoricalDataArray = factories.getStockHistoricalDataArray()
        stockHistoricalDataArray = json.json_keys_to_lower_and_snake_case(stockHistoricalDataArray)
        self.mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)
        historicalStockEntries = len(self.mongo.getStockHistoricalData(quote))
        self.assertEquals(len(stockHistoricalDataArray), historicalStockEntries)

    def testUpsertStockCurrentData_OK(self):
        quote = "BAC"
        currentData = self.mongo.getStockCurrentData(quote)
        self.assertIsNone(currentData)
        stockCurrentData = factories.getStockCurrentData()
        stockCurrentData = json.json_keys_to_lower_and_snake_case(stockCurrentData)
        self.mongo.upsertStockCurrentData(quote, stockCurrentData)
        currentData = self.mongo.getStockCurrentData(quote)
        currentData.pop("_id") # Remove MongoDB generated ID to match with stockCurrentData
        self.assertEquals(stockCurrentData, currentData)
