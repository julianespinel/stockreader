import unittest

import pymongo

from src.stocks import mongo


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
        stocks = [
            { "name": "Bank of America", "symbol": "BAC", "stockMarket": "NYSE" },
            { "name": "Tesla", "symbol": "TSLA", "stockMarket": "NASDAQ" },
            { "name": "Twitter", "symbol": "TWTR", "stockMarket": "NYSE" },
            { "name": "Facebook", "symbol": "FB", "stockMarket": "NASDAQ" }
        ]
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks), stockCount)

    def testSaveStockList_NOK_duplicateStock(self):
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = [
            { "name": "Bank of America", "symbol": "BAC", "stockMarket": "NYSE" },
            { "name": "Tesla", "symbol": "TSLA", "stockMarket": "NASDAQ" },
            { "name": "Tesla", "symbol": "TSLA", "stockMarket": "NASDAQ" },
            { "name": "Twitter", "symbol": "TWTR", "stockMarket": "NYSE" },
            { "name": "Facebook", "symbol": "FB", "stockMarket": "NASDAQ" }
        ]
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks) - 1, stockCount)

    def testStockExists_OK(self):
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = [
            {"name": "Twitter", "symbol": "TWTR", "stockMarket": "NYSE"},
            {"name": "Facebook", "symbol": "FB", "stockMarket": "NASDAQ"}
        ]
        self.mongo.saveStockList(stocks)
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(len(stocks), stockCount)
        self.assertTrue(self.mongo.stockExists("FB"))

    def testGetStockByQuote_OK(self):
        stockCount = len(self.mongo.readStocksFromStockList())
        self.assertEquals(0, stockCount)
        stocks = [
            { "name": "Twitter", "symbol": "TWTR", "stockMarket": "NYSE" },
            { "name": "Facebook", "symbol": "FB", "stockMarket": "NASDAQ" }
        ]
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
        self.mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)
        historicalStockEntries = len(self.mongo.getStockHistoricalData(quote))
        self.assertEquals(len(stockHistoricalDataArray), historicalStockEntries)

    def testUpsertStockCurrentData_OK(self):
        quote = "BAC"
        currentData = self.mongo.getStockCurrentData(quote)
        self.assertIsNone(currentData)
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
        self.mongo.upsertStockCurrentData(quote, stockCurrentData)
        currentData = self.mongo.getStockCurrentData(quote)
        currentData.pop("_id") # Remove MongoDB generated ID to match with stockCurrentData
        self.assertEquals(stockCurrentData, currentData)
