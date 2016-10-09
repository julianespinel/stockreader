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

    def __init__(self, domain, scheduler, time_series):
        self.domain = domain
        self.scheduler = scheduler
        self.time_series = time_series

    def get_number_of_workers(self, anyList):
        return len(anyList) if len(anyList) < self.WORKERS else self.WORKERS

    def download_and_save_stock_current_data_in_parallel(self, stocks):
        self.time_series.save_async("JOB", {}, { "method": "download_and_save_stock_current_data_in_parallel", "stocks": len(stocks) })
        number_of_workers = self.get_number_of_workers(stocks)
        with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
            for stock in stocks:
                executor.submit(self.domain.download_and_save_stock_current_data, stock)

    def download_and_save_stock_weekly_data_in_parallel(self, stocks):
        self.time_series.save_async("JOB", {}, { "method": "download_and_save_stock_weekly_data_in_parallel", "stocks": len(stocks) })
        today = date.today()
        initial_date = today - timedelta(weeks=self.WEEKS_AGO)
        number_of_workers = self.get_number_of_workers(stocks)
        with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
            for stock in stocks:
                executor.submit(self.domain.download_and_save_stock_historical_data, initial_date, today, stock)

    def download_and_save_stock_historical_data_in_parallel(self, stocks):
        self.time_series.save_async("JOB", {}, { "method": "download_and_save_stock_historical_data_in_parallel", "stocks": len(stocks) })
        today = date.today()
        # Here always use more workers because we need to perform more than one call.
        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            for stock in stocks:
                for index in range(self.YEARS_AGO):
                    initial_date = today.replace(year=(today.year - (index + 1)))
                    final_date = today.replace(year=(today.year - index))
                    executor.submit(self.domain.download_and_save_stock_historical_data, initial_date, final_date, stock)

    def schedule_stock_updates(self):
        stocks = self.domain.get_stock_list()
        self.scheduler.add_job(self.download_and_save_stock_current_data_in_parallel, 'cron', args=[stocks], hour='*')
        self.scheduler.add_job(self.download_and_save_stock_weekly_data_in_parallel, 'cron', args=[stocks], hour=self.DAILY_UPDATE_HOUR)
        self.scheduler.add_job(self.download_and_save_stock_historical_data_in_parallel, 'cron', args=[stocks], day='last', hour=self.MONTHLY_UPDATE_HOUR)
        self.scheduler.start()

    def add_stock_to_stockreader(self, stock):
        symbol = stock["symbol"]
        logger.info('adding stock %s', symbol)
        if not self.domain.stock_exists(symbol):
            self.domain.add_stock_to_stock_list(stock)
            self.download_and_save_stock_current_data_in_parallel([stock])
            self.download_and_save_stock_weekly_data_in_parallel([stock])
            self.download_and_save_stock_historical_data_in_parallel([stock])

    def add_stocks_list_to_stockreader(self, stocks):
        number_of_workers = self.get_number_of_workers(stocks)
        with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
            for stock in stocks:
                executor.submit(self.add_stock_to_stockreader, stock)
