import mongo
import download
import infrastructure as log
from datetime import date, timedelta

logger = log.getLogger("domain")

YEARS_AGO = 10

def downloadAndSaveStockCurrentData(stock):
    quote = stock["quote"]
    logger.info("stock %s", quote)
    stockCurrentData = download.getStockCurrentData(quote)
    mongo.saveStockCurrentData(quote, stockCurrentData)

def downloadAndSaveStockDataDaysFromToday(stock, daysFromToday):
    today = date.today()
    initialDate = today - timedelta(days=daysFromToday)
    quote = stock["quote"]
    logger.info("stock %s initialDate %s today %s", quote, initialDate, today)
    stockHistoricalDataArray = download.getStockHistoricalData(initialDate, today, quote)
    mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)

def downloadAndSaveStockHistoricalData(stock):
    today = date.today()
    quote = stock["quote"]
    for index in range(YEARS_AGO):
        initialDate = today.replace(year=(today.year-(index+1)))
        finalDate = today.replace(year=(today.year-index))
        logger.info("stock %s initialDate %s finalDate %s", quote, initialDate, finalDate)
        stockHistoricalDataArray = download.getStockHistoricalData(initialDate, finalDate, quote)
        mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)
