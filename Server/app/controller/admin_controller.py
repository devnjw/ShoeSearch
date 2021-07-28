from flask import request, jsonify, make_response
from flask_restful import Resource

from ..service.admin_service import get_searched_images

class AdminImage(Resource):
    def get(self):
        items = get_searched_images()
        return make_response(jsonify({'data':items}))