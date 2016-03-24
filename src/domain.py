import mongo
import download
from datetime import date

YEARS_AGO = 10

def downloadAndSaveStockCurrentData(stock):
    quote = stock["quote"]
    print("stock", quote)
    stockCurrentData = download.getStockCurrentData(quote)
    mongo.saveStockCurrentData(quote, stockCurrentData)

def downloadAndSaveStockHistoricalData(stock):
    today = date.today()
    quote = stock["quote"]
    for index in range(YEARS_AGO):
        initialDate = today.replace(year=(today.year-(index+1)))
        finalDate = today.replace(year=(today.year-index))
        print("stock", quote, "initialDate", initialDate, "finalDate", finalDate)
        stockHistoricalDataArray = download.getStockHistoricalData(initialDate, finalDate, quote)
        mongo.saveStockHistoricalData(quote, stockHistoricalDataArray)
