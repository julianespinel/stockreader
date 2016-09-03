import urllib
import requests
from infrastructure import json

class Download:

    def getStockHistoricalData(self, initialDate, finalDate, quote):
        baseUrl = "https://query.yahooapis.com/v1/public/yql"
        selectStatement = 'select * from yahoo.finance.historicaldata where symbol = "{quote}" and startDate = "{initialDate}" and endDate = "{finalDate}"'.format(quote=quote, initialDate=initialDate, finalDate=finalDate)
        query = urllib.parse.quote(selectStatement)
        resultFormat = 'json'
        env = urllib.parse.quote("store://datatables.org/alltableswithkeys")
        url = baseUrl + "?" + "q=" + query + "&format=" + resultFormat + "&env=" + env
        response = requests.get(url).json()
        count = response["query"]["count"]
        if count > 0:
            stockHistoricalDataArray = response["query"]["results"]["quote"]
        else:
            stockHistoricalDataArray = []
        stockHistoricalDataArray = json.json_keys_to_lower_and_snake_case(stockHistoricalDataArray)
        return stockHistoricalDataArray

    def getStockCurrentData(self, quote):
        baseUrl = "https://query.yahooapis.com/v1/public/yql"
        selectStatement = 'select * from yahoo.finance.quote where symbol in ("{quote}")'.format(quote=quote)
        query = urllib.parse.quote(selectStatement)
        resultFormat = 'json'
        env = urllib.parse.quote("store://datatables.org/alltableswithkeys")
        url = baseUrl + "?" + "q=" + query + "&format=" + resultFormat + "&env=" + env
        response = requests.get(url).json()
        count = response["query"]["count"]
        if count > 0:
            stockCurrentData = response["query"]["results"]["quote"]
        else:
            stockCurrentData = None
        stockCurrentData = json.json_keys_to_lower_and_snake_case(stockCurrentData)
        return stockCurrentData
