from flask import jsonify, make_response, request
from flask_restful import Resource

from .keyword_service import find_items_with_keyword
from .kpi_service import add_num_string_search, add_search_keyword_log

class ItemList(Resource):
    def get(self):
        keyword = request.args.get('keyword')
        if not keyword:
            keyword = ""
        
        add_num_string_search()
        add_search_keyword_log(keyword)
        
        items = find_items_with_keyword(keyword)

        resp = make_response(jsonify({'data':items}))

        # Header for CORS
        resp.headers["Access-Control-Allow-Origin"] = "*"

        return resp