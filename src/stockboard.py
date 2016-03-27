import sys
import job
import read
import mongo
import toml
import threading

NYSE = "nyse"
NASDAQ = "nasdaq"

def getConfig():
    # Read config parameters from a TOML file.
    config = None
    configFilePath = sys.argv[1]
    with open(configFilePath) as configFile:
        config = toml.loads(configFile.read())
    return config

config = getConfig()
stocks = read.readStocksFromExchangeFile(config, NYSE)
stocks.extend(read.readStocksFromExchangeFile(config, NASDAQ))
mongo.saveStockList(stocks)
print("stocks", len(stocks))

print("*********************************************************** 1")
schedule.every(1).hour.do(job.downloadAndSaveStockCurrentDataInParallel)
print("*********************************************************** 2")
schedule.every().day.at("18:00").do(job.downloadAndSaveStockWeeklyDataInParallel)
print("*********************************************************** 3")
schedule.every().saturday.at("23:00").do(job.downloadAndSaveStockHistoricalDataInParallel)
print("*********************************************************** 4")
while True:
    schedule.run_pending()
