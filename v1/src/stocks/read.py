import csv
from infrastructure import log

logger = log.get_logger("read")

class Read:

    def read_stocks_from_file(self, file_path, stock_market):
        stocks = []
        stocks_file = open(file_path)
        reader = csv.reader(stocks_file)
        next(reader) # Skip the first headers row.
        for row in reader:
            first_array = row[0].split("(")
            name = first_array[0].strip()
            second_array = first_array[1].split(")")
            quote = second_array[0].strip()
            stock = { "name": name, "symbol": quote, "stockMarket": stock_market}
            stocks.append(stock)
        return stocks

    def read_stocks_from_multiple_files(self, file_path_list, stock_market):
        stocks = []
        for file_path in file_path_list:
            stocks.extend(self.read_stocks_from_file(file_path, stock_market))
        return stocks
