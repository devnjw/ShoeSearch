from flask import jsonify, make_response
from flask_restful import Resource

from ..service.kpi_service import add_num_visit_home
from ..service.home_service import find_most_popular_items, find_most_popular_brands

class HomeKPI(Resource):
    def get(self):
        add_num_visit_home()
        return make_response(jsonify({'data':'Success'}))

class PopularItems(Resource):
    def get(self):
        items = find_most_popular_items()
        return make_response(jsonify({'data':items}))

class PopularBrands(Resource):
    def get(self):
        brands = find_most_popular_brands()
        print(brands)
        return make_response(jsonify({'data':brands}))