import pymongo
import infrastructure as log
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError

logger = log.getLogger("mongo")

client = MongoClient()
db = client["stockboarddb"]

# Do not use map and filter for side effects: http://stackoverflow.com/a/18433519/2420718
def saveStockList(stocks):
    if len(stocks) > 0:
        try:
            stocklistCollection = db["stocklist"]
            stocklistCollection.create_index([("quote", pymongo.ASCENDING)], unique=True)
            stocklistCollection.insert_many(stocks)
        except (DuplicateKeyError, BulkWriteError) as err:
            logger.error("saveStockList: %s", err)

def saveStockHistoricalData(quote, stockHistoricalDataArray):
    if len(stockHistoricalDataArray) > 0:
        try:
            stockHistoricalDataCollection = db[quote + "_historical_data"]
            stockHistoricalDataCollection.create_index([("Symbol", pymongo.ASCENDING), ("Date", pymongo.DESCENDING)], unique=True)
            stockHistoricalDataCollection.insert_many(stockHistoricalDataArray)
        except (DuplicateKeyError, BulkWriteError) as err:
            logger.error("saveStockHistoricalData: %s", err)

def upsertStockCurrentData(quote, stockCurrentData):
    if stockCurrentData is not None:
        try:
            stockCurrentDataCollection = db["stocks_current_data"]
            stockCurrentDataCollection.create_index([("symbol", pymongo.ASCENDING)], unique=True)
            query = {"symbol": quote}
            stockCurrentDataCollection.replace_one(query, stockCurrentData, upsert=True)
        except DuplicateKeyError as err:
            logger.error("saveStockCurrentData: %s", err)

def readStocksFromStockList():
    stocks = []
    stocklistCollection = db["stocklist"]
    cursor = stocklistCollection.find()
    for stock in cursor:
        stocks.append(stock)
    return stocks

def getStockByQuote(quote):
    stocklistCollection = db["stocklist"]
    stock = stocklistCollection.find_one({"quote": quote})
    return stock
