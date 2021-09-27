from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from .models import Item, Brand, SearchImages

class ItemSchema(ModelSchema):
    class Meta:
        model = Item

items_schema = ItemSchema(many=True)

class BrandSchema(ModelSchema):
    class Meta:
        model = Brand

brands_schema = BrandSchema(many=True)

class ImageSearchSchema(ModelSchema):
    class Meta:
        model = SearchImages

searched_images_schema = ImageSearchSchema(many=True)