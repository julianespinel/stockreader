import csv
from infrastructure import log

logger = log.get_logger("read")

class Read:

    def readStocksFromFile(self, filePath, stockMarket):
        stocks = []
        stocksFile = open(filePath)
        reader = csv.reader(stocksFile)
        next(reader) # Skip the first headers row.
        for row in reader:
            firstArray = row[0].split("(")
            name = firstArray[0].strip()
            secondArray = firstArray[1].split(")")
            quote = secondArray[0].strip()
            stock = { "name": name, "symbol": quote, "stockMarket": stockMarket }
            stocks.append(stock)
        return stocks

    def readStocksFromMultipleFiles(self, filePathList, stockMarket):
        stocks = []
        for filePath in filePathList:
            stocks.extend(self.readStocksFromFile(filePath, stockMarket))
        return stocks
