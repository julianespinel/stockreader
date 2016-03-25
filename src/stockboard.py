import sys
import job
import read
import mongo
import toml
import schedule

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
mongo.saveStockList(stocks)

print("*********************************************************** 1")
schedule.every().day.at("18:00").do(job.downloadAndSaveStockHistoricalDataInParallel)
print("*********************************************************** 2")
schedule.every(1).hour.do(job.downloadAndSaveStockCurrentDataInParallel)
print("*********************************************************** 2")
schedule.every().day.at("18:00").do(job.downloadAndSaveStockWeeklyDataInParallel)
print("*********************************************************** 3")
while True:
    schedule.run_pending()
