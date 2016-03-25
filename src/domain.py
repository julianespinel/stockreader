import mongo
import download
from datetime import date, timedelta

YEARS_AGO = 10

def downloadAndSaveStockCurrentData(stock):
    quote = stock["quote"]
    print("stock", quote)
    stockCurrentData = download.getStockCurrentData(quote)
    mongo.saveStockCurrentData(quote, stockCurrentData)

def downloadAndSaveStockDataDaysFromToday(stock, daysFromToday):
    today = date.today()
    initialDate = today - timedelta(days=daysFromToday)
    quote = stock["quote"]
    print("stock", quote, "initialDate", initialDate, "today", today)
    stockHistoricalDataArray = download.getStockHistoricalData(initialDate, today, quote)
    mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)

def downloadAndSaveStockHistoricalData(stock):
    today = date.today()
    quote = stock["quote"]
    for index in range(YEARS_AGO):
        initialDate = today.replace(year=(today.year-(index+1)))
        finalDate = today.replace(year=(today.year-index))
        print("stock", quote, "initialDate", initialDate, "finalDate", finalDate)
        stockHistoricalDataArray = download.getStockHistoricalData(initialDate, finalDate, quote)
        mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)
