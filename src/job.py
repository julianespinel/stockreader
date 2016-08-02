import time
import schedule
from concurrent.futures import ThreadPoolExecutor

class Job:

    WORKERS = 8
    DAYS_FROM_TODAY = 7

    def __init__(self, mongo, domain):
        self.mongo = mongo
        self.domain = domain

    def downloadAndSaveStockCurrentDataInParallel(self):
        stocks = self.mongo.readStocksFromStockList()
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockCurrentData, stock)

    def downloadAndSaveStockWeeklyDataInParallel(self):
        stocks = self.mongo.readStocksFromStockList()
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockDataDaysFromToday, stock, self.DAYS_FROM_TODAY)

    def downloadAndSaveStockHistoricalDataInParallel(self):
        stocks = self.mongo.readStocksFromStockList()
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockHistoricalData, stock)

    def updateStocks(self):
        schedule.every(1).hour.do(self.downloadAndSaveStockCurrentDataInParallel)
        schedule.every().day.at("18:00").do(self.downloadAndSaveStockWeeklyDataInParallel)
        schedule.every().saturday.at("23:00").do(self.downloadAndSaveStockHistoricalDataInParallel)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def addStockToStockreader(self, stock):
        self.mongo.saveStockList([stock])
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            executor.submit(self.domain.downloadAndSaveStockCurrentData, stock)
            executor.submit(self.domain.downloadAndSaveStockDataDaysFromToday, stock, self.DAYS_FROM_TODAY)
            executor.submit(self.domain.downloadAndSaveStockHistoricalData, stock)
