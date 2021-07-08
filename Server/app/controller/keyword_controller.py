from flask import jsonify, make_response, request
from flask_restful import Resource

from ..service.keyword_service import find_items_with_keyword
from ..service.kpi_service import add_num_string_search, add_search_keyword_log

class KeywordSearch(Resource):
    def get(self):
        keyword = request.args.get('keyword')
        if not keyword:
            keyword = ""
        
        add_num_string_search()
        add_search_keyword_log(keyword)
        
        items = find_items_with_keyword(keyword)

        return make_response(jsonify({'data':items}))