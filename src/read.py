import csv

def readStocksFromFile(filePath, stockMarket):
    stocks = []
    stocksFile = open(filePath)
    reader = csv.reader(stocksFile)
    next(reader) # Skip the first headers row.
    for row in reader:
        firstArray = row[0].split("(")
        name = firstArray[0].strip()
        secondArray = firstArray[1].split(")")
        quote = secondArray[0].strip()
        stock = { "name": name, "quote": quote, "stockMarket": stockMarket }
        stocks.append(stock)
    return stocks

def readStocksFromMultipleFiles(filePathList, stockMarket):
    stocks = []
    for filePath in filePathList:
        stocks.extend(readStocksFromFile(filePath, stockMarket))
    return stocks

def readStocksFromExchangeFile(config, exchange):
    exchangeFilePathList = config[exchange]
    stocksFromExchange = readStocksFromMultipleFiles(exchangeFilePathList, exchange)
    return stocksFromExchange
