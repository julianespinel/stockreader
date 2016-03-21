import sys
import load
import save
import toml
import download
from datetime import date

def getConfig():
    # Load config parameters from a TOML file.
    config = None
    configFilePath = sys.argv[1]
    with open(configFilePath) as configFile:
        config = toml.loads(configFile.read())
    return config

config = getConfig()
# NYSE Stocks
nyse = "nyse"
nyseFilePathList = config[nyse]
print(nyse, nyseFilePathList)
stocks = load.readStocksFromMultipleFiles(nyseFilePathList, nyse)
# NASDAQ Stocks
nasdaq = "nasdaq"
nasdaqFilePathList = config[nasdaq]
print(nasdaq, nasdaqFilePathList)
stocks.extend(load.readStocksFromMultipleFiles(nasdaqFilePathList, nasdaq))
print("stocks", len(stocks))
save.saveStockList(stocks)

# Download and save stock current data.
for stock in stocks:
    quote = stock["quote"]
    print("stock", quote)
    stockCurrentData = download.getStockCurrentData(quote)
    save.saveStockCurrentData(quote, stockCurrentData)

# Download and save stock historical data.
yearsAgo = 10
today = date.today()
initialDate = today.replace(year=today.year-yearsAgo)
for stock in stocks:
    quote = stock["quote"]
    for index in range(yearsAgo):
        initialDate = today.replace(year=(today.year-index))
        finalDate = today.replace(year=(today.year-index+1))
        print("stock", quote, "initialDate", initialDate, "finalDate", finalDate)
        stockHistoricalDataArray = download.getStockHistoricalData(initialDate, finalDate, quote)
        save.saveStockHistoricalData(quote, stockHistoricalDataArray)
