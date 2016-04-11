import sys
import job
import read
import mongo
import toml
import threading
import infrastructure as log

from flask import Flask
from flask_restful import Api
from api import StockAPI

NYSE = "nyse"
NASDAQ = "nasdaq"

logger = log.getLogger("reader")

def getConfig():
    # Read config parameters from a TOML file.
    config = None
    configFilePath = sys.argv[1]
    with open(configFilePath) as configFile:
        config = toml.loads(configFile.read())
    return config

config = getConfig()
exchanges = config["exchanges"]
stocks = read.readStocksFromExchangeFile(exchanges, NYSE)
stocks.extend(read.readStocksFromExchangeFile(exchanges, NASDAQ))
mongo.saveStockList(stocks)
logger.info("stocks %s", len(stocks))

jobsThread = threading.Thread(target=job.updateStocks)
jobsThread.start()

# Start the flask server
app = Flask(__name__)
api = Api(app)
api.add_resource(StockAPI, "/stockboard/api/stocks")

server = config["server"]
host = server["host"]
port = server["port"]
debug = server["debug"]
app.run(host=host, port=port, debug=debug)
