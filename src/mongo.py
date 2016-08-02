import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
import infrastructure as log

logger = log.getLogger("mongo")

class Mongo:

    def __init__(self, dbHost, dbPort, dbName):
        client = MongoClient(dbHost, dbPort)
        self.db = client[dbName]

    # Do not use map and filter for side effects: http://stackoverflow.com/a/18433519/2420718
    def saveStockList(self, stocks):
        if len(stocks) > 0:
            try:
                stocklistCollection = self.db["stocklist"]
                stocklistCollection.create_index([("quote", pymongo.ASCENDING)], unique=True)
                stocklistCollection.insert_many(stocks)
            except (DuplicateKeyError, BulkWriteError) as err:
                logger.error("saveStockList: %s", err)

    def readStocksFromStockList(self):
        stocks = []
        stocklistCollection = self.db["stocklist"]
        cursor = stocklistCollection.find()
        for stock in cursor:
            stocks.append(stock)
        return stocks

    def getStockByQuote(self, quote):
        stocklistCollection = self.db["stocklist"]
        stock = stocklistCollection.find_one({"quote": quote})
        return stock

    def saveStockHistoricalData(self, quote, stockHistoricalDataArray):
        if len(stockHistoricalDataArray) > 0:
            try:
                stockHistoricalDataCollection = self.db[quote + "_historical_data"]
                stockHistoricalDataCollection.create_index([("Symbol", pymongo.ASCENDING), ("Date", pymongo.DESCENDING)], unique=True)
                stockHistoricalDataCollection.insert_many(stockHistoricalDataArray)
            except (DuplicateKeyError, BulkWriteError) as err:
                logger.error("saveStockHistoricalData: %s", err)

    def getStockHistoricalData(self, quote):
        stockHistoricalDataCollection = self.db[quote + "_historical_data"]
        tradingDaysInOneYear = 252
        cursor = stockHistoricalDataCollection.find({ "Symbol": quote }).limit(tradingDaysInOneYear)
        return list(cursor)

    def upsertStockCurrentData(self, quote, stockCurrentData):
        if stockCurrentData is not None:
            try:
                stockCurrentDataCollection = self.db["stocks_current_data"]
                stockCurrentDataCollection.create_index([("symbol", pymongo.ASCENDING)], unique=True)
                query = {"symbol": quote}
                stockCurrentDataCollection.replace_one(query, stockCurrentData, upsert=True)
            except DuplicateKeyError as err:
                logger.error("saveStockCurrentData: %s", err)

    def getStockCurrentData(self, quote):
        stockCurrentDataCollection = self.db["stocks_current_data"]
        stock = stockCurrentDataCollection.find_one({ "symbol": quote })
        return stock
