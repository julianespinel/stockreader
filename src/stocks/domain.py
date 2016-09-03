from infrastructure import log
from datetime import date, timedelta

logger = log.getLogger("domain")

class Domain:

    def __init__(self, mongo, download):
        self.mongo = mongo
        self.download = download

    def downloadAndSaveStockCurrentData(self, stock):
        quote = stock["quote"]
        logger.info("stock %s", quote)
        stockCurrentData = self.download.getStockCurrentData(quote)
        self.mongo.upsertStockCurrentData(quote, stockCurrentData)

    def downloadAndSaveStockHistoricalData(self, initialDate, finalDate, stock):
        quote = stock["quote"]
        stockHistoricalDataArray = self.download.getStockHistoricalData(initialDate, finalDate, quote)
        self.mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)

    def stockExists(self, quote):
        return self.mongo.stockExists(quote)

    def getStockList(self):
        return self.mongo.readStocksFromStockList()

    def addStockToStockList(self, stock):
        self.mongo.saveStockList([stock])
