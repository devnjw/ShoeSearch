from flask import jsonify, make_response
from flask_restful import Resource

from ..service.kpi_service import add_num_visit_home

class HomeKPI(Resource):
    def get(self):
        add_num_visit_home()
        return make_response(jsonify({'data':'Success'}))