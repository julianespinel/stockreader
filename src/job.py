import mongo
import domain
from concurrent.futures import ThreadPoolExecutor

WORKERS = 8

def downloadAndSaveStockHistoricalDataInParallel():
    stocks = mongo.readStocksFromStockList()
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for stock in stocks:
            executor.submit(domain.downloadAndSaveStockHistoricalData, stock)

def downloadAndSaveStockCurrentDataInParallel():
    stocks = mongo.readStocksFromStockList()
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for stock in stocks:
            executor.submit(domain.downloadAndSaveStockCurrentData, stock)
