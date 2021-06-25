from flask import render_template, jsonify, make_response, request
from flask_restful import Resource, abort

from app import db
from app.models import Item
from .serializer import items_schema

class ItemList(Resource):
    def get(self):
        keyword = request.args.get('search')
        if not keyword:
            keyword = ""
        keyword = "%" + keyword + "%"
        
        output = Item.query\
            .filter(Item.title.like(keyword) | Item.brand.like(keyword))\
            .limit(100).all()
        output = items_schema.dump(output)

        resp = make_response(jsonify({'data':output}))

        # Header for CORS
        resp.headers["Access-Control-Allow-Origin"] = "*"

        return resp