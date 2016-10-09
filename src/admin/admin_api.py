from flask import Blueprint, jsonify
from infrastructure import log

logger = log.get_logger("admin_api")

def get_admin_blueprint(time_series):
    admin_blueprint = Blueprint('admin_api', __name__)

    @admin_blueprint.route('/ping')
    def ping():
        logger.info("ping")
        time_series.save_async("API", {}, { "method": "ping" })
        return jsonify({ "message": "pong" }), 200

    return admin_blueprint
