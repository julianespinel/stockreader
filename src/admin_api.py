from flask import request
from flask_restful import Resource

import infrastructure as log

logger = log.getLogger("admin_api")

class AdminAPI(Resource):
    def get(self):
        response = { "message": "pong" }, 200
        return response
