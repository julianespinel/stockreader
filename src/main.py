import load
import save

filePath = "../resources/NYSE-Most-Active-Stocks-2016-03-14.csv"
stocks = load.readStocks(filePath)
print(len(stocks))
save.saveStockList(stocks)


