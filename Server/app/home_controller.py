from flask import jsonify, make_response
from flask_restful import Resource

from .kpi_service import add_num_visit_home

class HomeKPI(Resource):
    def get(self):
        add_num_visit_home()

        resp = make_response(jsonify({'data':'Success'}))

        # Header for CORS
        resp.headers["Access-Control-Allow-Origin"] = "*"

        return resp