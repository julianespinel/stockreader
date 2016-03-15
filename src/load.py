import csv
import save

def readStocks(filePath):
    stocks = []
    stocksFile = open(filePath)
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

filePath = "../resources/NYSE-Most-Active-Stocks-2016-03-14.csv"
stocks = readStocks(filePath)
print(len(stocks))
save.saveStockList(stocks)
