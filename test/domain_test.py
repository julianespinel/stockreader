import unittest
import test.factories as factories

from datetime import date
from unittest.mock import Mock

from src.stocks import domain


class DomainTest(unittest.TestCase):

    def setUp(self):
        self.mongo_mock = Mock()
        self.download_mock = Mock()
        self.domain = domain.Domain(self.mongo_mock, self.download_mock)

    def test_download_and_save_stock_current_data_OK(self):
        stock = factories.get_stock_data()
        quote = stock["symbol"]
        stock_current_data = factories.get_stock_current_data()
        self.download_mock.get_stock_current_data = Mock(return_value=stock_current_data)
        self.mongo_mock.upsert_stock_current_data = Mock()
        self.domain.download_and_save_stock_current_data(stock)
        self.download_mock.get_stock_current_data.assert_called_once_with(quote)
        self.mongo_mock.upsert_stock_current_data.assert_called_once_with(quote, stock_current_data)

    def test_download_and_save_stock_current_data_NOK_empty_stock_current_data(self):
        stock = factories.get_stock_data()
        quote = stock["symbol"]
        stock_current_data = None
        self.download_mock.get_stock_current_data = Mock(return_value=stock_current_data)
        self.mongo_mock.upsert_stock_current_data = Mock()
        self.domain.download_and_save_stock_current_data(stock)
        self.download_mock.get_stock_current_data.assert_called_once_with(quote)
        self.mongo_mock.upsert_stock_current_data.assert_called_once_with(quote, stock_current_data)

    def test_download_and_save_stock_historical_data_OK(self):
        initial_date = date(2006, 9, 1)
        final_date = date(2016, 9, 1)
        stock = factories.get_stock_data()
        quote = stock["symbol"]
        stock_historical_data_array = factories.get_stock_historical_data_array()
        self.download_mock.get_stock_historical_data = Mock(return_value=stock_historical_data_array)
        self.mongo_mock.save_stock_historical_data = Mock()
        self.domain.download_and_save_stock_historical_data(initial_date, final_date, stock)
        self.download_mock.get_stock_historical_data.assert_called_once_with(initial_date, final_date, quote)
        self.mongo_mock.save_stock_historical_data.assert_called_once_with(quote, stock_historical_data_array)

    def test_download_and_save_stock_historical_data_NOK_empty_stock_historical_data_array(self):
        initial_date = date(2006, 9, 1)
        final_date = date(2016, 9, 1)
        stock = factories.get_stock_data()
        quote = stock["symbol"]
        stock_historical_data_array = []
        self.download_mock.get_stock_historical_data = Mock(return_value=stock_historical_data_array)
        self.mongo_mock.save_stock_historical_data = Mock()
        self.domain.download_and_save_stock_historical_data(initial_date, final_date, stock)
        self.download_mock.get_stock_historical_data.assert_called_once_with(initial_date, final_date, quote)
        self.mongo_mock.save_stock_historical_data.assert_called_once_with(quote, stock_historical_data_array)

    def test_stock_exists_OK(self):
        quote = "BAC"
        expected_result = True
        self.mongo_mock.stock_exists = Mock(return_value=expected_result)
        self.assertEqual(expected_result, self.domain.stock_exists(quote))
        self.mongo_mock.stock_exists.assert_called_once_with(quote)

    def test_stock_exists_NOK_stock_does_not_exist(self):
        quote = "BAC"
        expected_result = False
        self.mongo_mock.stock_exists = Mock(return_value=expected_result)
        self.assertEqual(expected_result, self.domain.stock_exists(quote))
        self.mongo_mock.stock_exists.assert_called_once_with(quote)

    def test_get_stock_list_OK(self):
        expected_stock_list = factories.get_stock_list()
        self.mongo_mock.read_stocks_from_stock_list = Mock(return_value=expected_stock_list)
        stock_list = self.domain.get_stock_list()
        self.assertEqual(len(expected_stock_list), len(stock_list))
        self.mongo_mock.read_stocks_from_stock_list.assert_called_once_with()

    def test_get_stock_list_NOK_empty_stock_list(self):
        expected_stock_list = []
        self.mongo_mock.read_stocks_from_stock_list = Mock(return_value=expected_stock_list)
        stock_list = self.domain.get_stock_list()
        self.assertEqual(len(expected_stock_list), len(stock_list))
        self.mongo_mock.read_stocks_from_stock_list.assert_called_once_with()

    def test_add_stock_to_stock_list_OK(self):
        stock = factories.get_stock_data()
        self.mongo_mock.save_stock_list = Mock()
        self.domain.add_stock_to_stock_list(stock)
        self.mongo_mock.save_stock_list.assert_called_once_with([stock])
