import unittest
import pymongo
import test.factories as factories

from src.stocks import mongo
from src.infrastructure import json

class MongoTest(unittest.TestCase):

    DB_HOST = "localhost"
    DB_PORT = 27017
    TEST_DB_NAME = "test_stockreader_db"

    def setUp(self):
        self.mongo = mongo.Mongo(self.DB_HOST, self.DB_PORT, self.TEST_DB_NAME)

    def tearDown(self):
        mongo_client = pymongo.MongoClient()
        mongo_client.drop_database(self.TEST_DB_NAME)

    def test_save_stock_list_OK(self):
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(0, stock_count)
        stocks = factories.get_stock_list()
        self.mongo.save_stock_list(stocks)
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(len(stocks), stock_count)

    def test_save_stock_list_NOK_duplicate_stock(self):
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(0, stock_count)
        stocks = factories.get_stock_list()
        stocks.append(stocks[0])
        self.mongo.save_stock_list(stocks)
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(len(stocks) - 1, stock_count)

    def test_stock_exists_OK(self):
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(0, stock_count)
        stocks = factories.get_stock_list()
        self.mongo.save_stock_list(stocks)
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(len(stocks), stock_count)
        self.assertTrue(self.mongo.stock_exists("FB"))

    def test_stock_exists_NOK_empty_stock_list(self):
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(0, stock_count)
        stocks = []
        self.mongo.save_stock_list(stocks)
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(len(stocks), stock_count)
        self.assertFalse(self.mongo.stock_exists("FB"))

    def test_get_stock_by_quote_OK(self):
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(0, stock_count)
        stocks = factories.get_stock_list()
        self.mongo.save_stock_list(stocks)
        stock_count = len(self.mongo.read_stocks_from_stock_list())
        self.assertEquals(len(stocks), stock_count)
        expected_stock = stocks[0]
        stock_by_quote = self.mongo.get_stock_by_quote(expected_stock["symbol"])
        self.assertEquals(expected_stock, stock_by_quote)

    def test_save_stock_historical_data_OK(self):
        quote = "BAC"
        historical_stock_entries = len(self.mongo.get_stock_historical_data(quote))
        self.assertEquals(0, historical_stock_entries)
        stock_historical_data_array = factories.get_stock_historical_data_array()
        stock_historical_data_array = json.json_keys_to_lower_and_snake_case(stock_historical_data_array)
        self.mongo.save_stock_historical_data(quote, stock_historical_data_array)
        historical_stock_entries = len(self.mongo.get_stock_historical_data(quote))
        self.assertEquals(len(stock_historical_data_array), historical_stock_entries)

    def test_upsert_stock_current_data_OK(self):
        quote = "BAC"
        current_data = self.mongo.get_stock_current_data(quote)
        self.assertIsNone(current_data)
        stock_current_data = factories.get_stock_current_data()
        stock_current_data = json.json_keys_to_lower_and_snake_case(stock_current_data)
        self.mongo.upsert_stock_current_data(quote, stock_current_data)
        current_data = self.mongo.get_stock_current_data(quote)
        current_data.pop("_id") # Remove MongoDB generated ID to match with stock_current_data
        self.assertEquals(stock_current_data, current_data)
