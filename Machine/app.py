from flask import Flask
from flask import request
from PIL import Image

from machine import FeatureExtractor
fe = FeatureExtractor()

app = Flask(__name__) 

@app.route('/image/feature', methods = ['POST'])
def get_feature():
    file = request.files['file']

    img = Image.open(file)

    # Extract features of Input Image
    feature = fe.extract(img)

    return feature

if __name__ == '__main__':
    app.run(debug=True, port=5090)