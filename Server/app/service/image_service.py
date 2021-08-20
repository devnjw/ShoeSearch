from PIL import Image
import numpy as np
import uuid
import os

from sqlalchemy.sql.expression import case

from app import fe, max_item_num

from app.models import Item
from ..serializer import items_schema

from .kpi_service import add_search_image_log

def find_items_with_image(file):
    similar_image_id_list = findSimilarImages(file)

    # Make order list to keep query result sorted
    ordering = case(
        {id: index for index, id in enumerate(similar_image_id_list)},
        value=Item.id
    )
    
    output = Item.query\
        .filter(Item.id.in_(similar_image_id_list))\
        .order_by(ordering)\
        .limit(max_item_num).all()
    output = items_schema.dump(output)

    return output

# input: image
# output: similar image ids
def findSimilarImages(img):
    img = Image.open(img)
    
    # Pre-extracted features of Database Images
    features = fe.features

    # Extract features of Input Image
    feature = fe.extract(img)

    # Calculate the similarity (distance) between images
    dists = np.linalg.norm(features - feature, axis=1)

    # Extract 100 images that have lowest distance
    ids = np.argsort(dists)[:max_item_num] + 1 # Type: numpy.int64

    return ids

def save_image(img):
    img = Image.open(img)
    
    # JPG does not support transparency
    img = img.convert('RGB')

    FILENAME = str(uuid.uuid4()) + ".jpg"
    FILEPATH = os.getcwd() + '/app/static/images/'

    os.makedirs(FILEPATH, exist_ok=True)
    img.save(os.path.join(FILEPATH, FILENAME))

    # Save name of image on DB
    add_search_image_log('/static/images/' + FILENAME)