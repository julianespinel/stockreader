import threading

from flask import request, Blueprint, jsonify

import infrastructure as log

logger = log.getLogger("stocks_api")

def get_stocks_blueprint(domain, job):
    stocks_api = Blueprint('/stocks', __name__)

    @stocks_api.route('', methods=['POST'])
    def add_stock():
        response = None
        newStock = request.get_json()
        if newStock is None:
            response = jsonify({ "error": "Please provide a stock in the request body. It should have a name, a quote and a stock market" }), 400
            return response
        name = newStock.get("name", None)
        quote = newStock.get("quote", None)
        logger.info("post: %s", newStock)
        stockMarket = newStock.get("stockMarket", None)
        isValidStock = name and quote and stockMarket
        if not isValidStock:
            response = jsonify({ "error": "Please provide a valid stock. It should have a name, a quote and a stock market" }), 400
            return response
        # This validation (stockExistInDB) should be performed in the domain level, not in the API level.
        stockExistInDB = domain.stockExists(quote)
        if stockExistInDB:
            response = jsonify({ "error": "The given stock already exists" }), 409
            return response
        # Add stock async
        thread = threading.Thread(target=job.addStockToStockreader, args=(newStock, )) # Why args should be a tuple?
        thread.start()
        response = jsonify({ "success": "The stock " + quote + " is being added" }), 202
        return response

    return stocks_api