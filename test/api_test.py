import unittest
from unittest.mock import Mock

from flask import Flask, json
from flask import request
from flask_restful import Api

from .context import src
from src import api

class ApiTest(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        flaskApi = Api()
        self.mongoMock = Mock()
        self.jobMock = Mock()
        flaskApi.add_resource(api.StockAPI, "/stockboard/api/stocks",
                              resource_class_kwargs={"mongo": self.mongoMock, "job": self.jobMock})
        flaskApi.init_app(app)
        self.client = app.test_client()

    def testAddStock_NOK_badRequest(self):
        response = self.client.post("/stockboard/api/stocks")
        self.assertEquals(response.status_code, 400)
        data = json.loads(response.data)
        expectedErrorMessage = "Please provide a valid stock. It should contain a name, a quote and a stock market"
        self.assertEquals(expectedErrorMessage, data["error"])
