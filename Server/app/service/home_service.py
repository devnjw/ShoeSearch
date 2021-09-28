from app import db
from ..models import Item, Brand
from ..serializer import items_schema, brands_schema

def find_most_popular_items(num_items=4):
    output = Item.query\
        .order_by(Item.clicked.desc())\
        .limit(num_items).all()
    output = items_schema.dump(output)

    return output

def find_most_popular_brands(num_items=4):
    output = Brand.query\
        .order_by(Brand.clicked.desc())\
        .limit(num_items).all()
    output = brands_schema.dump(output)

    return output