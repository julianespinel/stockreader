import time
import schedule
import mongo
import domain
from concurrent.futures import ThreadPoolExecutor

WORKERS = 8
DAYS_FROM_TODAY = 7

def downloadAndSaveStockCurrentDataInParallel():
    stocks = mongo.readStocksFromStockList()
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for stock in stocks:
            executor.submit(domain.downloadAndSaveStockCurrentData, stock)

def downloadAndSaveStockWeeklyDataInParallel():
    stocks = mongo.readStocksFromStockList()
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for stock in stocks:
            executor.submit(domain.downloadAndSaveStockDataDaysFromToday, stock, DAYS_FROM_TODAY)

def downloadAndSaveStockHistoricalDataInParallel():
    stocks = mongo.readStocksFromStockList()
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for stock in stocks:
            executor.submit(domain.downloadAndSaveStockHistoricalData, stock)

def updateStocks(stocks):
    print("*********************************************************** 1")
    schedule.every(1).hour.do(downloadAndSaveStockCurrentDataInParallel)
    print("*********************************************************** 2")
    schedule.every().day.at("18:00").do(downloadAndSaveStockWeeklyDataInParallel)
    print("*********************************************************** 3")
    schedule.every().saturday.at("23:00").do(downloadAndSaveStockHistoricalDataInParallel)
    print("*********************************************************** 4")
    while True:
        schedule.run_pending()
        time.sleep(1)
