import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError

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
            print("saveStockList: ", err)

def saveStockHistoricalData(quote, stockHistoricalDataArray):
    if len(stockHistoricalDataArray) > 0:
        try:
            stockHistoricalDataCollection = db[quote + "_historical_data"]
            stockHistoricalDataCollection.create_index([("Symbol", pymongo.ASCENDING), ("Date", pymongo.DESCENDING)], unique=True)
            stockHistoricalDataCollection.insert_many(stockHistoricalDataArray)
        except (DuplicateKeyError, BulkWriteError) as err:
            print("saveStockHistoricalData: ", err)

def saveStockCurrentData(quote, stockCurrentData):
    if stockCurrentData is not None:
        try:
            stockCurrentDataCollection = db["stocks_current_data"]
            stockCurrentDataCollection.create_index([("symbol", pymongo.ASCENDING)], unique=True)
            stockCurrentDataCollection.insert_one(stockCurrentData)
        except DuplicateKeyError as err:
            print("saveStockCurrentData: ", err)
