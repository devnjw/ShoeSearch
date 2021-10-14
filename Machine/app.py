from flask import Flask, request, jsonify, make_response
import numpy as np
from PIL import Image

from machine import FeatureExtractor
fe = FeatureExtractor()

app = Flask(__name__) 

# Todo: Test API transaction cost
@app.route('/image/feature', methods = ['POST'])
def get_feature():
    file = request.files['file']

    img = Image.open(file)

    # Extract features of Input Image
    feature = fe.extract(img)
    # feature = feature.tolist()

    # Pre-extracted features of Database Images
    features = fe.features

    # Extract features of Input Image
    # feature = fe.extract(img)

    # Calculate the similarity (distance) between images
    dists = np.linalg.norm(features - feature, axis=1)

    # Extract 100 images that have lowest distance
    ids = np.argsort(dists)[:96] + 1 # Type: numpy.int64
    ids = ids.tolist()

    return make_response(jsonify({'data':ids}))

if __name__ == '__main__':
    app.run(debug=True, port=5090)