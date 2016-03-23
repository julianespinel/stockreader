import sys
import read
import save
import toml
import domain
from concurrent.futures import ThreadPoolExecutor

def getConfig():
    # Read config parameters from a TOML file.
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
stocks = read.readStocksFromMultipleFiles(nyseFilePathList, nyse)
# NASDAQ Stocks
nasdaq = "nasdaq"
nasdaqFilePathList = config[nasdaq]
print(nasdaq, nasdaqFilePathList)
stocks.extend(read.readStocksFromMultipleFiles(nasdaqFilePathList, nasdaq))
print("stocks", len(stocks))
save.saveStockList(stocks)

workers = 8
with ThreadPoolExecutor(max_workers=workers) as executor:
    for stock in stocks:
        executor.submit(domain.downloadAndSaveStockCurrentData, stock)
        executor.submit(domain.downloadAndSaveStockHistoricalData, stock)
