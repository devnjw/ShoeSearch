from flask import render_template, jsonify, make_response, request
from flask_restful import Resource, abort
from sqlalchemy import any_

from app import db, max_item_num
from ..models import Item, Brand
from ..serializer import items_schema

def find_items_with_keyword(keyword):
    # If keyword is consisted with multiple words
    if len(keyword.split()) >= 2:
        return find_items_with_keywords(keyword)

    keyword = "%" + keyword + "%"

    output = Item.query\
        .join(Brand, Item.brand==Brand.eng_name)\
        .add_columns(Item.title, Item.brand, Brand.subs, Item.image_url, Item.item_url, Item.price, Item.shop, Item.title)\
        .filter(Item.title.like(keyword) | Item.brand.like(keyword) | Brand.subs.like(keyword))\
        .limit(max_item_num).all()
    output = items_schema.dump(output)

    return output

def find_items_with_keywords(keywords):
    keyword_list = keywords.split()

    for i in range(len(keyword_list)):
        keyword_list[i] = "%" + keyword_list[i] + "%"

    output = Item.query\
        .join(Brand, Item.brand==Brand.eng_name)\
        .add_columns(Item.title, Item.brand, Brand.subs, Item.image_url, Item.item_url, Item.price, Item.shop, Item.title)

    for i in range(len(keyword_list)):
        output = output.filter(Item.title.like(keyword_list[i]) | Item.brand.like(keyword_list[i]) | Brand.subs.like(keyword_list[i]))
        
    output = output.limit(max_item_num).all()
    output = items_schema.dump(output)

    return output