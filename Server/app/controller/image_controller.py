from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.sql.expression import case

from app.models import Item
from ..serializer import items_schema

from ..service.image_service import findSimilarImages, save_image
from ..service.kpi_service import add_num_image_search

class ImageSearch(Resource):
    def post(self):
        file = request.files['file']

        similar_image_id_list = findSimilarImages(file)
        
        # Log image search
        save_image(file)
        add_num_image_search()

        # Make order list to keep query result sorted
        ordering = case(
            {id: index for index, id in enumerate(similar_image_id_list)},
            value=Item.id
        )
        
        output = Item.query\
            .filter(Item.id.in_(similar_image_id_list))\
            .order_by(ordering)\
            .limit(100).all()
        output = items_schema.dump(output)

        return make_response(jsonify({'data':output}))