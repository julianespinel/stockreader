import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
from infrastructure import log

logger = log.get_logger("mongo")

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
        self.create_regular_collection_if_not_exists(self.STOCK_LIST, self.SYMBOL_KEY)
        self.create_regular_collection_if_not_exists(self.STOCKS_CURRENT_DATA, self.SYMBOL_KEY)

    # Do not use map and filter for side effects: http://stackoverflow.com/a/18433519/2420718
    def save_stock_list(self, stocks):
        if len(stocks) > 0:
            try:
                stocklist_collection = self.db[self.STOCK_LIST]
                stocklist_collection.insert_many(stocks, ordered=False)
            except (DuplicateKeyError, BulkWriteError) as err:
                logger.error("save_stock_list: %i %s", len(stocks), err)

    def read_stocks_from_stock_list(self):
        stocks = []
        stocklist_collection = self.db[self.STOCK_LIST]
        cursor = stocklist_collection.find()
        for stock in cursor:
            stocks.append(stock)
        return stocks

    def stock_exists(self, quote):
        stock_current_data_collection = self.db[self.STOCK_LIST]
        cursor = stock_current_data_collection.find({ self.SYMBOL_KEY: quote }).limit(1)
        return (cursor.count() > 0)

    def get_stock_by_quote(self, quote):
        stocklist_collection = self.db[self.STOCK_LIST]
        stock = stocklist_collection.find_one({ self.SYMBOL_KEY: quote })
        return stock

    def save_stock_historical_data(self, quote, stock_historical_data_array):
        if len(stock_historical_data_array) > 0:
            try:
                collection_name = quote + self.HISTORICAL_DATA_SUFIX
                self.create_historical_collection_if_not_exists(collection_name)
                stock_historical_data_collection = self.db[collection_name]
                stock_historical_data_collection.insert_many(stock_historical_data_array, ordered=False)
            except (DuplicateKeyError, BulkWriteError) as err:
                logger.error("save_stock_historical_data: %s %i %s", quote, len(stock_historical_data_array), err)

    def get_stock_historical_data(self, quote):
        stock_historical_data_collection = self.db[quote + self.HISTORICAL_DATA_SUFIX]
        cursor = stock_historical_data_collection.find({ self.SYMBOL_KEY: quote }).limit(self.TRADING_DAYS_PER_YEAR)
        return list(cursor)

    def upsert_stock_current_data(self, quote, stock_current_data):
        if stock_current_data is not None:
            try:
                stock_current_data_collection = self.db[self.STOCKS_CURRENT_DATA]
                query = { self.SYMBOL_KEY: quote }
                stock_current_data_collection.replace_one(query, stock_current_data, upsert=True)
            except DuplicateKeyError as err:
                logger.error("upsert_stock_current_data: %s %s", quote, err)

    def get_stock_current_data(self, quote):
        stockCurrentDataCollection = self.db[self.STOCKS_CURRENT_DATA]
        stock = stockCurrentDataCollection.find_one({ self.SYMBOL_KEY: quote })
        return stock
