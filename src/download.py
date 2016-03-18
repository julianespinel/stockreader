import urllib
import requests

baseUrl = "https://query.yahooapis.com/v1/public/yql"
query = urllib.parse.quote('select * from yahoo.finance.historicaldata where symbol = "YHOO" and startDate = "2015-03-11" and endDate = "2016-03-11"')
resultFormat = 'json'
env = urllib.parse.quote("store://datatables.org/alltableswithkeys")
url = baseUrl + "?" + "q=" + query + "&format=" + resultFormat + "&env=" + env
response = requests.get(url)
print(response.url)
print(response.content)
