import csv

def readStocks(stocksFile):
    stocks = []
    reader = csv.reader(stocksFile)
    next(reader) # Skip the first headers row.
    for row in reader:
        firstArray = row[0].split("(")
        name = firstArray[0].strip()
        secondArray = firstArray[1].split(")")
        quote = secondArray[0].strip()
        stock = { "name": name, "quote": quote }
        stocks.append(stock)
    return stocks

def getReadFromFile(filePath, readerFunction):
    fileToRead = open(filePath)
    return readerFunction(fileToRead)

filePath = "../resources/NYSE-Most-Active-Stocks-2016-03-14.csv"
stocks = getReadFromFile(filePath, readStocks)
print(stocks)
