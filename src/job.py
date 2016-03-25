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
