from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor
from infrastructure import log

logger = log.get_logger("job")

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
                executor.submit(self.domain.download_and_save_stock_current_data, stock)

    def downloadAndSaveStockWeeklyDataInParallel(self, stocks):
        today = date.today()
        initialDate = today - timedelta(weeks=self.WEEKS_AGO)
        numberOfWorkers = self.getNumberOfWorkers(stocks)
        with ThreadPoolExecutor(max_workers=numberOfWorkers) as executor:
            for stock in stocks:
                executor.submit(self.domain.download_and_save_stock_historical_data, initialDate, today, stock)

    def downloadAndSaveStockHistoricalDataInParallel(self, stocks):
        today = date.today()
        # Here always use more workers because we need to perform more than one call.
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                for index in range(self.YEARS_AGO):
                    initialDate = today.replace(year=(today.year - (index + 1)))
                    finalDate = today.replace(year=(today.year - index))
                    executor.submit(self.domain.download_and_save_stock_historical_data, initialDate, finalDate, stock)

    def scheduleStockUpdates(self):
        stocks = self.domain.get_stock_list()
        self.scheduler.add_job(self.downloadAndSaveStockCurrentDataInParallel, 'cron', args=[stocks], hour='*')
        self.scheduler.add_job(self.downloadAndSaveStockWeeklyDataInParallel, 'cron', args=[stocks], hour=self.DAILY_UPDATE_HOUR)
        self.scheduler.add_job(self.downloadAndSaveStockHistoricalDataInParallel, 'cron', args=[stocks], day='last', hour=self.MONTHLY_UPDATE_HOUR)
        self.scheduler.start()

    def addStockToStockreader(self, stock):
        symbol = stock["symbol"]
        logger.info('adding stock %s', symbol)
        if not self.domain.stock_exists(symbol):
            self.domain.add_stock_to_stock_list(stock)
            self.downloadAndSaveStockCurrentDataInParallel([stock])
            self.downloadAndSaveStockWeeklyDataInParallel([stock])
            self.downloadAndSaveStockHistoricalDataInParallel([stock])

    def addStocksListToStockreader(self, stocks):
        for stock in stocks:
            self.addStockToStockreader(stock)
