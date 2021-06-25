import os, uuid
from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Resource, abort

class ImageUpload(Resource):
    def post(self):
        file = request.files['file']
        
        FILENAME = str(uuid.uuid4()) + ".jpg"
        FILEPATH = os.getcwd() + '/app/static/images/'

        os.makedirs(FILEPATH, exist_ok=True)
        file.save(os.path.join(FILEPATH, FILENAME))

        return redirect(url_for('itemlist'))
        # return jsonify({'result': "Image Uploaded Successfully"})