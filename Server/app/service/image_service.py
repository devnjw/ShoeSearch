from PIL import Image
import numpy as np
import uuid
import os

import requests

from sqlalchemy.sql.expression import case
from flask_restful import abort

from app import fe, max_item_num, db

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

    # url = "http://127.0.0.1:5090/image/feature"
    # file = {'file': img}
    # res = requests.post(url, files=file).json()
    # # feature = res['data']

    # ids = res['data']
    
    # # Pre-extracted features of Database Images
    # features = fe.features

    # # Extract features of Input Image
    # # feature = fe.extract(img)

    # # Calculate the similarity (distance) between images
    # dists = np.linalg.norm(features - feature, axis=1)

    # # Extract 100 images that have lowest distance
    # ids = np.argsort(dists)[:max_item_num] + 1 # Type: numpy.int64

    items = Item.query.with_entities(Item.id, Item.feature).all()

    feature = fe.extract(img)
    feature *= 10000
    feature = feature.astype(int)

    dists = []
    for item in items:
        try:
            if item.feature:
                tmp = []
                tmp.append(item.id)
                f = np.fromstring(item.feature, dtype=int, sep=" ")
                dist = np.linalg.norm(feature - f)
                tmp.append(dist)
                dists.append(tmp)
        except Exception as e:
            pass

    dists.sort(key=lambda x:x[1])
    
    ids = np.array(dists)[:max_item_num,0]

    return ids

def save_all_image_feature():
    items = Item.query.order_by(Item.id.desc()).all()
    cnt = 1
    for item in items:
        print(cnt, "/", len(items))
        cnt += 1
        save_image_feature(item.id)

def save_image_feature(id):
    try:
        item = Item.query.filter_by(id=id).first()
        img = Image.open(requests.get(item.image_url, stream=True).raw)

        
        features = fe.extract(img)
        features *= 10000
        features = features.astype(int)

        str_feature = ""
        for feature in features:
            str_feature += str(feature) + " "

        item.feature = str_feature

        db.session.commit()

    except Exception as e:
        print(e)

def save_image(img):
    img = Image.open(img)
    
    # JPG does not support transparency
    img = img.convert('RGB')

    FILENAME = str(uuid.uuid4()) + ".jpg"
    FILEPATH = os.getcwd() + '/../Admin/static/image_logs/'

    os.makedirs(FILEPATH, exist_ok=True)
    img.save(os.path.join(FILEPATH, FILENAME))

    # Save name of image on DB
    add_search_image_log('/static/image_logs/' + FILENAME)