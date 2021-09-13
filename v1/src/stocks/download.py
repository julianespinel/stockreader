import urllib
import requests
from infrastructure import json
from infrastructure import log

logger = log.get_logger("download")

class Download:

    def get_stock_historical_data(self, initialDate, finalDate, quote):
        stock_historical_data_array = []
        base_url = "https://query.yahooapis.com/v1/public/yql"
        select_statement = 'select * from yahoo.finance.historicaldata where symbol = "{quote}" and startDate = "{initialDate}" and endDate = "{finalDate}"'.format(quote=quote, initialDate=initialDate, finalDate=finalDate)
        query = urllib.parse.quote(select_statement)
        result_format = 'json'
        env = urllib.parse.quote("store://datatables.org/alltableswithkeys")
        url = base_url + "?" + "q=" + query + "&format=" + result_format + "&env=" + env
        response = requests.get(url)
        status_code = response.status_code
        body = response.json()
        if status_code == 200:
            count = body["query"]["count"]
            if count > 0:
                stock_historical_data_array = body["query"]["results"]["quote"]
                stock_historical_data_array = json.json_keys_to_lower_and_snake_case(stock_historical_data_array)
        else:
            logger.error("get_stock_historical_data: status_code: %i, body: %s", status_code, body)
        return stock_historical_data_array

    def get_stock_current_data(self, quote):
        stock_current_data = None
        base_url = "https://query.yahooapis.com/v1/public/yql"
        select_statement = 'select * from yahoo.finance.quote where symbol in ("{quote}")'.format(quote=quote)
        query = urllib.parse.quote(select_statement)
        result_format = 'json'
        env = urllib.parse.quote("store://datatables.org/alltableswithkeys")
        url = base_url + "?" + "q=" + query + "&format=" + result_format + "&env=" + env
        response = requests.get(url)
        status_code = response.status_code
        body = response.json()
        if status_code == 200:
            count = body["query"]["count"]
            if count > 0:
                stock_current_data = body["query"]["results"]["quote"]
                stock_current_data = json.json_keys_to_lower_and_snake_case(stock_current_data)
        else:
            logger.error("get_stock_current_data: status_code: %i, body: %s", status_code, body)
        return stock_current_data
