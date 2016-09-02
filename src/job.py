from concurrent.futures import ThreadPoolExecutor

class Job:

    WORKERS = 8
    DAYS_FROM_TODAY = 7

    def __init__(self, domain, scheduler):
        self.domain = domain
        self.scheduler = scheduler

    def downloadAndSaveStockCurrentDataInParallel(self):
        stocks = self.domain.getStockList()
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockCurrentData, stock)

    def downloadAndSaveStockWeeklyDataInParallel(self):
        stocks = self.domain.getStockList()
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockDataDaysFromToday, stock, self.DAYS_FROM_TODAY)

    def downloadAndSaveStockHistoricalDataInParallel(self):
        stocks = self.domain.getStockList()
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockHistoricalData, stock)

    def updateStocks(self):
        self.scheduler.add_job(self.downloadAndSaveStockCurrentDataInParallel, 'cron', hour='*')
        self.scheduler.add_job(self.downloadAndSaveStockWeeklyDataInParallel, 'cron', hour=18)
        self.scheduler.add_job(self.downloadAndSaveStockHistoricalDataInParallel, 'cron', day='last', hour=23)
        self.scheduler.start()

    def addStockToStockreader(self, stock):
        self.mongo.saveStockList([stock])
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            executor.submit(self.domain.downloadAndSaveStockCurrentData, stock)
            executor.submit(self.domain.downloadAndSaveStockDataDaysFromToday, stock, self.DAYS_FROM_TODAY)
            executor.submit(self.domain.downloadAndSaveStockHistoricalData, stock)
