import unittest
from unittest.mock import Mock

from flask import Flask, json

from src.stocks import stocks_api


class ApiTest(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        self.domainMock = Mock()
        self.jobMock = Mock()
        stocks_blueprint = stocks_api.get_stocks_blueprint(self.domainMock, self.jobMock)
        app.register_blueprint(stocks_blueprint, url_prefix='/stockreader/api/stocks')
        self.client = app.test_client()

    def testAddStock_NOK_emptyRequestBody(self):
        response = self.client.post("/stockreader/api/stocks")
        self.assertEquals(response.status_code, 400)
        data = json.loads(response.data)
        expectedErrorMessage = "Please provide a stock in the request body. It should have a name, a quote and a stock market"
        self.assertEquals(expectedErrorMessage, data["error"])

    def testAddStock_NOK_notValidStock(self):
        stock = { "name": "Bank of America", "quote": "", "stockMarket": "" }
        response = self.client.post("/stockreader/api/stocks", data=json.dumps(stock), content_type="application/json")
        self.assertEquals(response.status_code, 400)
        data = json.loads(response.data)
        expectedErrorMessage = "Please provide a valid stock. It should have a name, a quote and a stock market"
        self.assertEquals(expectedErrorMessage, data["error"])

    def testAddStock_NOK_existingStock(self):
        self.domainMock.stockExists = Mock(return_value=True)
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        response = self.client.post("/stockreader/api/stocks", data=json.dumps(stock), content_type="application/json")
        self.domainMock.stockExists.assert_called_once_with(quote)
        self.assertEquals(response.status_code, 409)
        data = json.loads(response.data)
        expectedErrorMessage = "The given stock already exists"
        self.assertEquals(expectedErrorMessage, data["error"])

    def testAddStock_OK(self):
        self.domainMock.stockExists = Mock(return_value=False)
        quote = "BAC"
        stock = { "name": "Bank of America", "quote": quote, "stockMarket": "NYSE" }
        response = self.client.post("/stockreader/api/stocks", data=json.dumps(stock), content_type="application/json")
        self.domainMock.stockExists.assert_called_once_with(quote)
        self.assertEquals(response.status_code, 202)
        data = json.loads(response.data)
        expectedMessage = "The stock " + quote + " is being added"
        self.assertEquals(expectedMessage, data["success"])

