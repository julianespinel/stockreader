import unittest

from src.infrastructure import json

class JsonTest(unittest.TestCase):

    def test_json_keys_to_lower_case_OK_single_element(self):
        element = {
            "Adj_Close": "13.79",
            "Date": "2016-03-18",
            "Close": "13.79",
            "Volume": "145037500",
            "Open": "13.68",
            "Low": "13.55",
            "High": "13.88",
            "Symbol": "BAC"
        }
        json_lower_case_keys = json.json_keys_to_lower_and_snake_case(element)
        # Check structure
        self.assertEqual(len(element.keys()), len(json_lower_case_keys.keys()))
        # Check values
        self.assertEqual(element["Adj_Close"], json_lower_case_keys["adj_close"])
        self.assertEqual(element["Date"], json_lower_case_keys["date"])
        self.assertEqual(element["Close"], json_lower_case_keys["close"])
        self.assertEqual(element["Volume"], json_lower_case_keys["volume"])
        self.assertEqual(element["Open"], json_lower_case_keys["open"])
        self.assertEqual(element["Low"], json_lower_case_keys["low"])
        self.assertEqual(element["High"], json_lower_case_keys["high"])
        self.assertEqual(element["Symbol"], json_lower_case_keys["symbol"])

    def test_json_keys_to_lower_case_OK_single_element_with_duplicated_key(self):
        # The symbol and Symbol (lower and upper case) will be symbol after the method
        element = {
            "symbol": "YHOO",
            "AverageDailyVolume": "11160200",
            "Change": "+0.35",
            "DaysLow": "43.08",
            "DaysHigh": "43.60",
            "YearLow": "26.15",
            "YearHigh": "43.60",
            "MarketCapitalization": "41.19B",
            "LastTradePriceOnly": "43.28",
            "DaysRange": "43.08 - 43.60",
            "Name": "Yahoo! Inc.",
            "Symbol": "YHOO",
            "Volume": "7339013",
            "StockExchange": "NMS"
        }
        json_lower_case_keys = json.json_keys_to_lower_and_snake_case(element)
        # Check structure
        self.assertEqual(len(element.keys()) - 1, len(json_lower_case_keys.keys()))
        # Check values
        self.assertEqual(element["symbol"], json_lower_case_keys["symbol"])
        self.assertEqual(element["AverageDailyVolume"], json_lower_case_keys["average_daily_volume"])
        self.assertEqual(element["Change"], json_lower_case_keys["change"])
        self.assertEqual(element["DaysLow"], json_lower_case_keys["days_low"])
        self.assertEqual(element["DaysHigh"], json_lower_case_keys["days_high"])
        self.assertEqual(element["YearLow"], json_lower_case_keys["year_low"])
        self.assertEqual(element["YearHigh"], json_lower_case_keys["year_high"])
        self.assertEqual(element["MarketCapitalization"], json_lower_case_keys["market_capitalization"])
        self.assertEqual(element["LastTradePriceOnly"], json_lower_case_keys["last_trade_price_only"])
        self.assertEqual(element["DaysRange"], json_lower_case_keys["days_range"])
        self.assertEqual(element["Name"], json_lower_case_keys["name"])
        self.assertEqual(element["Symbol"], json_lower_case_keys["symbol"])
        self.assertEqual(element["Volume"], json_lower_case_keys["volume"])
        self.assertEqual(element["StockExchange"], json_lower_case_keys["stock_exchange"])

    def test_json_keys_to_lower_case_OK_list(self):
        stockHistoricalDataArray = [
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
        json_list = json.json_keys_to_lower_and_snake_case(stockHistoricalDataArray)
        self.assertEqual(len(stockHistoricalDataArray), len(json_list))
        self.assertEqual(stockHistoricalDataArray[0]["Symbol"], json_list[0]["symbol"])