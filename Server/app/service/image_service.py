from PIL import Image
import numpy as np
import uuid
import os

import requests

from sqlalchemy.sql.expression import case
from flask_restful import abort

from app import fe, max_item_num, db

from app.models import Item, SimilarItems
from ..serializer import items_schema

from .kpi_service import add_search_image_log

def find_items_with_graph_search(file, depth=10, num=100, pick=10):
    img = Image.open(file)

    feature = fe.extract(img)
    
    similar_image_id_list = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 2026])

    new_list = []
    
    for i in range(depth):
        # Make order list to keep query result sorted
        ordering = case(
            {id: index for index, id in enumerate(similar_image_id_list)},
            value=SimilarItems.item_id
        )
        
        sim_items = SimilarItems.query\
            .filter(SimilarItems.item_id.in_(similar_image_id_list))\
            .order_by(ordering)\
            .all()

        new_list = []

        for item in sim_items:
            sim_ids = np.fromstring(item.sim_items, dtype=int, sep=" ")
            for id in sim_ids:
                new_list.append(id)

        new_list = np.array(new_list)
        
        items = Item.query\
            .with_entities(Item.id, Item.feature)\
            .filter(Item.id.in_(new_list))\
            .all()
        
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
        
        similar_image_id_list = np.array(dists)[:pick,0]
    
    # Make order list to keep query result sorted
    ordering = case(
        {id: index for index, id in enumerate(new_list)},
        value=Item.id
    )
    
    output = Item.query\
        .filter(Item.id.in_(new_list))\
        .order_by(ordering)\
        .limit(max_item_num).all()
    output = items_schema.dump(output)

    print(len(output))

    return output

def save_all_similar_items():
    print("Started to get items")
    items = Item.query.with_entities(Item.id, Item.feature).all()
    
    #extract all features from string to int
    print("For loop started")
    for item in items:
        if item.id < 2902:
            continue
        try:
            print(item.id, "/", len(items))
            save_similar_items(items, item)
        except Exception as e:
            pass
        # dists = []
        # for i in items:
        #     try:
        #         if item.id == i.id:
        #             continue

        #         feature = np.fromstring(item.feature, dtype=int, sep=" ")
        #         f = np.fromstring(i.feature, dtype=int, sep=" ")

        #         tmp = []
        #         tmp.append(i.id)
        #         dist = np.linalg.norm(feature - f)
        #         tmp.append(dist)
        #         dists.append(tmp)
                
        #     except Exception as e:
        #         pass

        # dists.sort(key=lambda x:x[1])

        # # print("dists:", dists)
        
        # ids = np.array(dists)[:10,0]

        # print(ids)



def save_similar_items(items, item):
    
    feature = np.fromstring(item.feature, dtype=int, sep=" ")

    similar_image_id_list = findSimilarImages(limit=10, items=items, feature=feature)

    str_sim_item_ids = ""
    for id in similar_image_id_list:
        str_sim_item_ids += str(int(id)) + " "

    try:
        
        new_item = SimilarItems(
            item_id = item.id,
            sim_items = str_sim_item_ids
        )

        db.session.add(new_item)
        db.session.commit()

    except Exception as e:
        print(e)


def find_items_with_image(file):
    img = Image.open(file)

    similar_image_id_list = findSimilarImages(img)

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
def findSimilarImages(img=None, limit=100, items=[], feature=[], id=None):
    if not items:
        items = Item.query.with_entities(Item.id, Item.feature).all()

    if type(feature) is not np.ndarray:
        feature = fe.extract(img)

    dists = []
    for item in items:
        if id is not None and id == item.id:
            continue
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
    
    ids = np.array(dists)[:limit,0]

    print(type(ids), ids)

    return ids

def save_all_image_feature():
    items = Item.query.order_by(Item.id.desc()).all()
    for item in items:
        save_image_feature(item.id)

def save_image_feature(id):
    try:
        item = Item.query.filter_by(id=id).first()
        img = Image.open(requests.get(item.image_url, stream=True).raw)

        
        features = fe.extract(img)

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