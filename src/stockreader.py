import sys
import toml

from infrastructure import log
from admin import admin_api
from stocks import job, read, mongo, domain, download, stocks_api

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler

NYSE = "nyse"
NASDAQ = "nasdaq"

logger = log.getLogger("stockreader")

def getConfig():
    # Read config parameters from a TOML file.
    config = None
    configFilePath = sys.argv[1]
    with open(configFilePath) as configFile:
        config = toml.loads(configFile.read())
    return config

def readStocksFromExchangeFile(config, exchange):
    exchangeFilePathList = config[exchange]
    stocksFromExchange = read.readStocksFromMultipleFiles(exchangeFilePathList, exchange)
    return stocksFromExchange

# Initialize
config = getConfig()
mongoConfig = config["mongo"]
dbHost = mongoConfig["host"]
dbPort = mongoConfig["port"]
dbName = mongoConfig["name"]

mongo = mongo.Mongo(dbHost, dbPort, dbName)
read = read.Read()
download = download.Download()
domain = domain.Domain(mongo, download)

scheduler = BackgroundScheduler()
job = job.Job(domain, scheduler)

# add stocks from files.
exchanges = config["exchanges"]
stocks = readStocksFromExchangeFile(exchanges, NYSE)
stocks.extend(readStocksFromExchangeFile(exchanges, NASDAQ))
logger.info("stocks %s", len(stocks))
job.addStocksListToStockreader(stocks)

# Schedule recurrent stock update jobs.
job.scheduleStockUpdates()

# Start the flask server
app = Flask(__name__)
admin_blueprint = admin_api.get_admin_blueprint()
app.register_blueprint(admin_blueprint, url_prefix='/stockreader/admin')
stocks_api = stocks_api.get_stocks_blueprint(domain, job)
app.register_blueprint(stocks_api, url_prefix='/stockreader/api/stocks')

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
