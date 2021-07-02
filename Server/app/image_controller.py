import os, uuid
from flask import Flask, request, jsonify, redirect, url_for, make_response
from flask_restful import Resource, abort
from sqlalchemy.sql.expression import case

from app import db
from app.models import Item
from .serializer import items_schema

from .image_service import findSimilarImages, save_image
from .kpi_service import add_num_image_search

class ImageUpload(Resource):
    def post(self):
        file = request.files['file']
        
        FILENAME = str(uuid.uuid4()) + ".jpg"
        FILEPATH = os.getcwd() + '/app/static/images/'

        os.makedirs(FILEPATH, exist_ok=True)
        file.save(os.path.join(FILEPATH, FILENAME))

        return jsonify({'result': "Image Uploaded Successfully"})


class ImageSearch(Resource):
    def post(self):
        file = request.files['file']

        similar_image_id_list = findSimilarImages(file)
        
        # save image log
        save_image(file)

        add_num_image_search()

        ordering = case(
            {id: index for index, id in enumerate(similar_image_id_list)},
            value=Item.id
        )
        
        output = Item.query\
            .filter(Item.id.in_(similar_image_id_list))\
            .order_by(ordering)\
            .limit(100).all()
        output = items_schema.dump(output)

        resp = make_response(jsonify({'data':output}))

        # Header for CORS
        resp.headers["Access-Control-Allow-Origin"] = "*"

        return resp