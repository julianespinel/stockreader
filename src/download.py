import urllib
import requests
from datetime import date

def getStockHistoricalData(initialDate, finalDate, quote):
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
    return stockHistoricalDataArray

def getStockCurrentData(quote):
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
    return stockCurrentData
