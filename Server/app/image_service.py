from PIL import Image
import numpy as np
import uuid
import os

from app import fe

from .kpi_service import add_search_image_log

# input: image
# output: similar image ids
def findSimilarImages(img):
    img = Image.open(img)
    
    features = fe.features

    # Extract its features
    query = fe.extract(img)

    # Calculate the similarity (distance) between images
    dists = np.linalg.norm(features - query, axis=1)

    # Extract 100 images that have lowest distance
    ids = np.argsort(dists)[:100] + 1 # Type: numpy.int64

    return ids

def save_image(img):
    img = Image.open(img)

    FILENAME = str(uuid.uuid4()) + ".jpg"
    FILEPATH = os.getcwd() + '/app/static/images/'

    os.makedirs(FILEPATH, exist_ok=True)
    img.save(os.path.join(FILEPATH, FILENAME))

    add_search_image_log('/static/images/' + FILENAME)