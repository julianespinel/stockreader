from pymongo import MongoClient

client = MongoClient()
db = client["stockboarddb"]

# Do not use map and filter for side effects: http://stackoverflow.com/a/18433519/2420718
def saveStockList(stocks):
    stocklistCollection = db["stocklist"]
    for stock in stocks:
        stockExists = (stocklistCollection.count(stock) > 0)
        if not stockExists:
            stocklistCollection.insert_one(stock)
