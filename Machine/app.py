from flask import Flask, jsonify
from flask import request
import json, os

from .machine import FeatureExtractor
fe = FeatureExtractor()

app = Flask(__name__) 

@app.route('/image/similarity', methods = ['POST'])
def image_save():
    file = request.files['file']

    FILENAME = "test.jpg"
    FILEPATH = os.getcwd() + '/static/images/'

    os.makedirs(FILEPATH, exist_ok=True)
    file.save(os.path.join(FILEPATH, FILENAME))

    result = {'data': "Image Uploaded Successfully"}
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True, port=5050)s