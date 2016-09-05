from infrastructure import log
from datetime import date, timedelta

logger = log.get_logger("domain")

class Domain:

    def __init__(self, mongo, download):
        self.mongo = mongo
        self.download = download

    def download_and_save_stock_current_data(self, stock):
        quote = stock["symbol"]
        logger.info("stock %s", quote)
        stock_current_data = self.download.get_stock_current_data(quote)
        self.mongo.upsertStockCurrentData(quote, stock_current_data)

    def download_and_save_stock_historical_data(self, initialDate, finalDate, stock):
        quote = stock["symbol"]
        logger.info('stocks %s, %s, %s', initialDate, finalDate, quote)
        stock_historical_data_array = self.download.get_stock_historical_data(initialDate, finalDate, quote)
        self.mongo.saveStockHistoricalData(quote, stock_historical_data_array)

    def stock_exists(self, quote):
        return self.mongo.stock_exists(quote)

    def get_stock_list(self):
        return self.mongo.readStocksFromStockList()

    def add_stock_to_stock_list(self, stock):
        self.mongo.saveStockList([stock])
