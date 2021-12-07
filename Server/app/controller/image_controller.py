from flask import request, jsonify, make_response
from flask_restful import Resource

from ..service.image_service import find_items_with_image, save_image, save_all_similar_items, find_items_with_graph_search
from ..service.kpi_service import add_num_image_search

class ImageSearch(Resource):
    def post(self):
        file = request.files['file']

        add_num_image_search()

        items = find_items_with_image(file)

        try:
            # Log image search
            save_image(file)
        except Exception as e:
            print(e)

        return make_response(jsonify({'data':items}))

class SimilarImages(Resource):
    def get(self):
        print("request started")
        save_all_similar_items()

        return make_response(jsonify({'data':'Success'}))

class GraphImageSearch(Resource):
    def post(self):
        file = request.files['file']

        add_num_image_search()

        items = find_items_with_graph_search(file)

        try:
            # Log image search
            save_image(file)
        except Exception as e:
            print(e)

        return make_response(jsonify({'data':items})) 