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

jobsThread = threading.Thread(target=job.updateStocks, args=(stocks, )) # Why args should be a tuple?
jobsThread.start()

print("*********************************************************** 5")
