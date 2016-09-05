from infrastructure import log
from datetime import date, timedelta

logger = log.get_logger("domain")

class Domain:

    def __init__(self, mongo, download):
        self.mongo = mongo
        self.download = download

    def downloadAndSaveStockCurrentData(self, stock):
        quote = stock["symbol"]
        logger.info("stock %s", quote)
        stockCurrentData = self.download.getStockCurrentData(quote)
        self.mongo.upsertStockCurrentData(quote, stockCurrentData)

    def downloadAndSaveStockHistoricalData(self, initialDate, finalDate, stock):
        quote = stock["symbol"]
        logger.info('stocks %s, %s, %s', initialDate, finalDate, quote)
        stockHistoricalDataArray = self.download.getStockHistoricalData(initialDate, finalDate, quote)
        self.mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)

    def stockExists(self, quote):
        return self.mongo.stockExists(quote)

    def getStockList(self):
        return self.mongo.readStocksFromStockList()

    def addStockToStockList(self, stock):
        self.mongo.saveStockList([stock])
