from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor

class Job:

    WEEKS_AGO = 1
    YEARS_AGO = 10

    WORKERS = 8
    LESS_WORKERS = 3
    DAYS_FROM_TODAY = 7

    DAILY_UPDATE_HOUR = 18
    MONTHLY_UPDATE_HOUR = 23

    def __init__(self, domain, scheduler):
        self.domain = domain
        self.scheduler = scheduler

    def getNumberOfWorkers(self, anyList):
        return len(anyList) if len(anyList) < self.WORKERS else self.WORKERS

    def downloadAndSaveStockCurrentDataInParallel(self, stocks):
        numberOfWorkers = self.getNumberOfWorkers(stocks)
        with ThreadPoolExecutor(max_workers=numberOfWorkers) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockCurrentData, stock)

    def downloadAndSaveStockWeeklyDataInParallel(self, stocks):
        today = date.today()
        initialDate = today - timedelta(weeks=self.WEEKS_AGO)
        numberOfWorkers = self.getNumberOfWorkers(stocks)
        with ThreadPoolExecutor(max_workers=numberOfWorkers) as executor:
            for stock in stocks:
                executor.submit(self.domain.downloadAndSaveStockHistoricalData, initialDate, today, stock)

    def downloadAndSaveStockHistoricalDataInParallel(self, stocks):
        today = date.today()
        # Here always use more workers because we need to perform more than one call.
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                for index in range(self.YEARS_AGO):
                    initialDate = today.replace(year=(today.year - (index + 1)))
                    finalDate = today.replace(year=(today.year - index))
                    executor.submit(self.domain.downloadAndSaveStockHistoricalData, initialDate, finalDate, stock)

    def scheduleStockUpdates(self):
        stocks = self.domain.getStockList()
        self.scheduler.add_job(self.downloadAndSaveStockCurrentDataInParallel, 'cron', args=[stocks], hour='*')
        self.scheduler.add_job(self.downloadAndSaveStockWeeklyDataInParallel, 'cron', args=[stocks], hour=self.DAILY_UPDATE_HOUR)
        self.scheduler.add_job(self.downloadAndSaveStockHistoricalDataInParallel, 'cron', args=[stocks], day='last', hour=self.MONTHLY_UPDATE_HOUR)
        self.scheduler.start()

    def addStockToStockreader(self, stock):
        if not self.domain.stockExists(stock["quote"]):
            self.domain.addStockToStockList(stock)
            self.downloadAndSaveStockCurrentDataInParallel([stock])
            self.downloadAndSaveStockWeeklyDataInParallel([stock])
            self.downloadAndSaveStockHistoricalDataInParallel([stock])

    def addStocksListToStockreader(self, stocks):
        for stock in stocks:
            self.addStockToStockreader(stock)
