import job
import mongo
import threading

from flask import request
from flask_restful import Resource

class StockAPI(Resource):

    def post(self):
        response = None
        print("****************************** 1")
        newStock = request.get_json()
        name = newStock.get("name", None)
        quote = newStock.get("quote", None)
        stockMarket = newStock.get("stockMarket", None)
        isValidStock = name and quote and stockMarket
        print("****************************** 2")
        if isValidStock:
            print("****************************** 3")
            stockExistInDB = mongo.getStockByQuote(quote)
            if (not stockExistInDB):
                print("****************************** 4")
                thread = threading.Thread(target=job.addStockToStockboard, args=(newStock, )) # Why args should be a tuple?
                thread.start()
                response = { "success": "The stock " + quote + " is being added" }, 202
            else:
                print("****************************** 5")
                response = { "error": "The given stock already exists" }, 409
        else:
            response = { "error": "Please provide a valid stock. It should contain a name, a quote and a stock market" }, 400
        return response
