import sys
import toml
import threading

import job
import read
import mongo
import domain
import download
import infrastructure as log
from api import StockAPI

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Flask
from flask_restful import Api

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

# Initialize
config = getConfig()
mongoConfig = config["mongo"]
dbName = mongoConfig["dbName"]
mongo = mongo.Mongo(dbName)
print(dbName)

download = download.Download()
domain = domain.Domain(mongo, download)
job = job.Job(mongo, domain)

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
api.add_resource(StockAPI, "/stockboard/api/stocks", resource_class_kwargs={"mongo": mongo, "job": job})
server = config["server"]
host = server["host"]
port = server["port"]
debug = server["debug"]
if debug:
    app.run(host=host, port=port, debug=debug)
else:
    http_server = HTTPServer(WSGIContainer(app))
    http_server.bind(port)
    http_server.start(0)  # forks one process per cpu.
    IOLoop.current().start()
