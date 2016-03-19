import urllib
import requests
from datetime import date


def getStockHistorycalData(quote, initialDate, finalDate):
    baseUrl = "https://query.yahooapis.com/v1/public/yql"
    selectStatement = 'select * from yahoo.finance.historicaldata where symbol = "{quote}" and startDate = "{initialDate}" and endDate = "{finalDate}"'.format(quote=quote, initialDate=initialDate, finalDate=finalDate)
    query = urllib.parse.quote(selectStatement)
    resultFormat = 'json'
    env = urllib.parse.quote("store://datatables.org/alltableswithkeys")
    url = baseUrl + "?" + "q=" + query + "&format=" + resultFormat + "&env=" + env
    response = requests.get(url)
    print(response.url)
    print(response.content)

quote = "YHOO"
today = date.today()
initialDate = today.replace(year=today.year-1)
finalDate = today
getStockHistorycalData(quote, initialDate, finalDate)
