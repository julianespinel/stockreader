import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
from infrastructure import log

logger = log.getLogger("mongo")

class Mongo:

    SYMBOL_KEY = "symbol"
    DATE_KEY = "date"

    TRADING_DAYS_PER_YEAR = 252

    STOCK_LIST = "stocklist"
    STOCKS_CURRENT_DATA = "stocks_current_data"
    HISTORICAL_DATA_SUFIX = "_historical_data"

    def collection_exists(self, collection_name):
        return collection_name in self.db.collection_names()

    def create_regular_collection_if_not_exists(self, collection_name, index_key):
        if not self.collection_exists(collection_name):
            collection = self.db[collection_name]
            collection.create_index([(index_key, pymongo.ASCENDING)], unique=True)

    def create_historical_collection_if_not_exists(self, collection_name):
        if not self.collection_exists(collection_name):
            collection = self.db[collection_name]
            collection.create_index([(self.SYMBOL_KEY, pymongo.ASCENDING), (self.DATE_KEY, pymongo.DESCENDING)], unique=True)

    def __init__(self, dbHost, dbPort, dbName):
        client = MongoClient(dbHost, dbPort)
        self.db = client[dbName]

    # Do not use map and filter for side effects: http://stackoverflow.com/a/18433519/2420718
    def saveStockList(self, stocks):
        if len(stocks) > 0:
            try:
                stocklistCollection = self.db["stocklist"]
                stocklistCollection.create_index([("quote", pymongo.ASCENDING)], unique=True)
                stocklistCollection.insert_many(stocks, ordered=False)
            except (DuplicateKeyError, BulkWriteError) as err:
                logger.error("saveStockList: %i %s", len(stocks), err)

    def readStocksFromStockList(self):
        stocks = []
        stocklistCollection = self.db["stocklist"]
        cursor = stocklistCollection.find()
        for stock in cursor:
            stocks.append(stock)
        return stocks

    def stockExists(self, quote):
        stockCurrentDataCollection = self.db["stocklist"]
        cursor = stockCurrentDataCollection.find({ "quote": quote }).limit(1)
        return (cursor.count() > 0)

    def getStockByQuote(self, quote):
        stocklistCollection = self.db["stocklist"]
        stock = stocklistCollection.find_one({"quote": quote})
        return stock

    def saveStockHistoricalData(self, quote, stockHistoricalDataArray):
        if len(stockHistoricalDataArray) > 0:
            try:
                stockHistoricalDataCollection = self.db[quote + "_historical_data"]
                stockHistoricalDataCollection.create_index([("Symbol", pymongo.ASCENDING), ("Date", pymongo.DESCENDING)], unique=True)
                stockHistoricalDataCollection.insert_many(stockHistoricalDataArray, ordered=False)
            except (DuplicateKeyError, BulkWriteError) as err:
                logger.error("saveStockHistoricalData: %s %i %s", quote, len(stockHistoricalDataArray), err)

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
