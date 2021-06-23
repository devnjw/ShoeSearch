from flask import render_template, jsonify, make_response
from flask_restful import Resource, abort

from app import db
from app.models import Item
from .serializer import items_schema

class ItemList(Resource):
    def get(self):
        output = Item.query.limit(20).all()
        output = items_schema.dump(output)
        print(output)

        #return make_response(render_template('result.html', query_string=output))

        resp = make_response(jsonify({'data':output}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
        
        # return jsonify({'data':output})