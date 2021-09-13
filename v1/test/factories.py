def get_stock_data():
    return {"name": "Bank of America", "symbol": "BAC", "stockMarket": "NYSE"}

def get_not_valid_stock_data():
    return { "name": "Bank of America", "symbol": "", "stockMarket": "" }

def get_stock_list():
    stock_list = [
        {"name": "Bank of America", "symbol": "BAC", "stockMarket": "NYSE"},
        {"name": "Tesla", "symbol": "TSLA", "stockMarket": "NASDAQ"},
        {"name": "Twitter", "symbol": "TWTR", "stockMarket": "NYSE"},
        {"name": "Facebook", "symbol": "FB", "stockMarket": "NASDAQ"},
        {"stockMarket": "nyse", "name": "Valspar", "symbol": "VAL"},
        {"stockMarket": "nyse", "name": "Trinseo", "symbol": "TSE"},
        {"stockMarket": "nyse", "name": "Celestica", "symbol": "CLS"}
    ]
    return stock_list

def get_stock_current_data():
    stock_current_data = {
        "symbol": "BAC",
        "DaysLow": "13.780",
        "StockExchange": "NYQ",
        "DaysRange": "13.780 - 13.940",
        "Volume": "3255146",
        "LastTradePriceOnly": "13.925",
        "YearHigh": "18.480",
        "MarketCapitalization": "146.44B",
        "Name": "Bank of America Corporation Com",
        "AverageDailyVolume": "136399008",
        "Change": "+0.135",
        "DaysHigh": "13.940",
        "Symbol": "BAC",
        "YearLow": "10.990"
    }
    return stock_current_data

def get_stock_historical_data_array():
    stock_historical_data_array = [
        {
            "Adj_Close": "13.79",
            "Date": "2016-03-18",
            "Close": "13.79",
            "Volume": "145037500",
            "Open": "13.68",
            "Low": "13.55",
            "High": "13.88",
            "Symbol": "BAC"
        },
        {
            "Adj_Close": "13.40",
            "Date": "2016-03-17",
            "Close": "13.40",
            "Volume": "121732700",
            "Open": "13.22",
            "Low": "13.05",
            "High": "13.48",
            "Symbol": "BAC"
        },
        {
            "Adj_Close": "13.31",
            "Date": "2016-03-16",
            "Close": "13.31",
            "Volume": "148489100",
            "Open": "13.51",
            "Low": "13.09",
            "High": "13.81",
            "Symbol": "BAC"
        }
    ]
    return stock_historical_data_array