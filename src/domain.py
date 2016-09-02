import infrastructure as log
from datetime import date, timedelta

logger = log.getLogger("domain")

class Domain:

    YEARS_AGO = 10

    def __init__(self, mongo, download):
        self.mongo = mongo
        self.download = download

    def downloadAndSaveStockCurrentData(self, stock):
        quote = stock["quote"]
        logger.info("stock %s", quote)
        stockCurrentData = self.download.getStockCurrentData(quote)
        self.mongo.upsertStockCurrentData(quote, stockCurrentData)

    def downloadAndSaveStockDataDaysFromToday(self, stock, daysFromToday):
        today = date.today()
        initialDate = today - timedelta(days=daysFromToday)
        quote = stock["quote"]
        logger.info("stock %s initialDate %s today %s", quote, initialDate, today)
        stockHistoricalDataArray = self.download.getStockHistoricalData(initialDate, today, quote)
        self.mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)

    def downloadAndSaveStockHistoricalData(self, stock):
        today = date.today()
        quote = stock["quote"]
        for index in range(self.YEARS_AGO):
            initialDate = today.replace(year=(today.year-(index+1)))
            finalDate = today.replace(year=(today.year-index))
            logger.info("stock %s initialDate %s finalDate %s", quote, initialDate, finalDate)
            stockHistoricalDataArray = self.download.getStockHistoricalData(initialDate, finalDate, quote)
            self.mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)

    def stockExists(self, quote):
        return self.mongo.stockExists(quote)

    def getStockList(self):
        return self.mongo.readStocksFromStockList()
