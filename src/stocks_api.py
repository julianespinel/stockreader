import threading

from flask import request
from flask_restful import Resource

import infrastructure as log

logger = log.getLogger("stocks_api")

class StocksAPI(Resource):

    def __init__(self, **kwargs):
        self.domain = kwargs["domain"]
        self.job = kwargs["job"]

    def post(self):
        response = None
        newStock = request.get_json()
        if newStock is None:
            response = { "error": "Please provide a stock in the request body. It should have a name, a quote and a stock market" }, 400
            return response
        name = newStock.get("name", None)
        quote = newStock.get("quote", None)
        logger.info("post: %s", newStock)
        stockMarket = newStock.get("stockMarket", None)
        isValidStock = name and quote and stockMarket
        if not isValidStock:
            response = { "error": "Please provide a valid stock. It should have a name, a quote and a stock market" }, 400
            return response
        # This validation (stockExistInDB) should be performed in the domain level, not in the API level.
        stockExistInDB = self.domain.stockExists(quote)
        if stockExistInDB:
            response = { "error": "The given stock already exists" }, 409
            return response
        # Add stock async
        thread = threading.Thread(target=self.job.addStockToStockreader, args=(newStock, )) # Why args should be a tuple?
        thread.start()
        response = { "success": "The stock " + quote + " is being added" }, 202
        return response
