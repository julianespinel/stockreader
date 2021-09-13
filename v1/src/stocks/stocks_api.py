import threading

from flask import request, Blueprint, jsonify
from infrastructure import log

logger = log.get_logger("stocks_api")

def get_stocks_blueprint(domain, job, time_series):
    stocks_blueprint = Blueprint('stocks_api', __name__)

    @stocks_blueprint.route('', methods=['POST'])
    def add_stock():
        response = None
        new_stock = request.get_json()
        logger.info("post: %s", new_stock)
        if new_stock is None:
            response = jsonify({ "error": "Please provide a stock in the request body. It should have a name, a symbol and a stock market" }), 400
            return response
        name = new_stock.get("name", None)
        quote = new_stock.get("symbol", None)
        stock_market = new_stock.get("stockMarket", None)
        is_valid_stock = name and quote and stock_market
        if not is_valid_stock:
            response = jsonify({ "error": "Please provide a valid stock. It should have a name, a symbol and a stock market" }), 400
            return response
        # This validation (stockExistInDB) should be performed in the domain level, not in the API level.
        stock_exist_in_db = domain.stock_exists(quote)
        if stock_exist_in_db:
            response = jsonify({ "error": "The given stock already exists" }), 409
            return response
        # Add stock async
        time_series.save_async("API", {}, { "method": "add_stock", "stock": quote })
        thread = threading.Thread(target=job.add_stock_to_stockreader, args=(new_stock,)) # Why args should be a tuple?
        thread.start()
        response = jsonify({ "success": "The stock " + quote + " is being added" }), 202
        return response

    return stocks_blueprint
