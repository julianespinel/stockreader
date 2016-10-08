import datetime
from concurrent.futures import ThreadPoolExecutor
from infrastructure import log

logger = log.get_logger("time_series")

class TimeSeries:

    DB_NAME = "stockreaderdb"
    NUMBER_OF_WORKERS = 5

    def __init__(self, influx_client):
        self.influx = influx_client
        self.influx.create_database(self.DB_NAME)
        self.influx.switch_database(self.DB_NAME)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.NUMBER_OF_WORKERS)

    def save_async(self, measurement, tags_dict, fields_dict):
        data = {
            "measurement": measurement,
            "tags": tags_dict,
            "time": datetime.datetime.now().isoformat(),
            "fields": fields_dict
        }
        points = [data]
        self.thread_pool.submit(self.influx.write_points, points)
