from flask import Flask, request, jsonify, make_response
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
    feature = feature.tolist()
    
    return make_response(jsonify({'data':feature}))

if __name__ == '__main__':
    app.run(debug=True, port=5090)