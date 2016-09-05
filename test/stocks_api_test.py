import unittest
from unittest.mock import Mock
import test.factories as factories

from flask import Flask, json

from src.stocks import stocks_api


class ApiTest(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        self.domain_mock = Mock()
        self.job_mock = Mock()
        stocks_blueprint = stocks_api.get_stocks_blueprint(self.domain_mock, self.job_mock)
        app.register_blueprint(stocks_blueprint, url_prefix='/stockreader/api/stocks')
        self.client = app.test_client()

    def test_add_stock_OK(self):
        stock = factories.get_stock_data()
        quote = stock["symbol"]
        self.domain_mock.stock_exists = Mock(return_value=False)
        response = self.client.post("/stockreader/api/stocks", data=json.dumps(stock), content_type="application/json")
        self.domain_mock.stock_exists.assert_called_once_with(quote)
        self.assertEquals(response.status_code, 202)
        data = json.loads(response.data)
        expected_message = "The stock " + quote + " is being added"
        self.assertEquals(expected_message, data["success"])

    def test_add_stock_NOK_empty_request_body(self):
        response = self.client.post("/stockreader/api/stocks")
        self.assertEquals(response.status_code, 400)
        data = json.loads(response.data)
        expected_error_message = "Please provide a stock in the request body. It should have a name, a symbol and a stock market"
        self.assertEquals(expected_error_message, data["error"])

    def test_add_stock_NOK_not_valid_stock(self):
        stock = factories.get_not_valid_stock_data()
        response = self.client.post("/stockreader/api/stocks", data=json.dumps(stock), content_type="application/json")
        self.assertEquals(response.status_code, 400)
        data = json.loads(response.data)
        expected_error_message = "Please provide a valid stock. It should have a name, a symbol and a stock market"
        self.assertEquals(expected_error_message, data["error"])

    def test_add_stock_NOK_existing_stock(self):
        stock = factories.get_stock_data()
        quote = stock["symbol"]
        self.domain_mock.stock_exists = Mock(return_value=True)
        response = self.client.post("/stockreader/api/stocks", data=json.dumps(stock), content_type="application/json")
        self.domain_mock.stock_exists.assert_called_once_with(quote)
        self.assertEquals(response.status_code, 409)
        data = json.loads(response.data)
        expected_error_message = "The given stock already exists"
        self.assertEquals(expected_error_message, data["error"])
