from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from .models import Item, SearchImages


class ItemSchema(ModelSchema):
    class Meta:
        model = Item

items_schema = ItemSchema(many=True)

class ImageSearchSchema(ModelSchema):
    class Meta:
        model = SearchImages

searched_images_schema = ImageSearchSchema(many=True)