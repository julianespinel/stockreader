import threading

from flask import request
from flask_restful import Resource

import infrastructure as log

logger = log.getLogger("api")

class StockAPI(Resource):

    def __init__(self, **kwargs):
        self.mongo = kwargs["mongo"]
        self.job = kwargs["job"]

    def post(self):
        response = None
        newStock = request.get_json()
        name = newStock.get("name", None)
        quote = newStock.get("quote", None)
        logger.info("post: %s", newStock)
        stockMarket = newStock.get("stockMarket", None)
        isValidStock = name and quote and stockMarket
        if isValidStock:
            stockExistInDB = self.mongo.getStockByQuote(quote)
            if (not stockExistInDB):
                thread = threading.Thread(target=self.job.addStockToStockboard, args=(newStock, )) # Why args should be a tuple?
                thread.start()
                response = { "success": "The stock " + quote + " is being added" }, 202
            else:
                response = { "error": "The given stock already exists" }, 409
        else:
            response = { "error": "Please provide a valid stock. It should contain a name, a quote and a stock market" }, 400
        return response
