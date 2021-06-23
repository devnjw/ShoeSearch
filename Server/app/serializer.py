from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from .models import Item


class ItemSchema(ModelSchema):
    class Meta:
        model = Item

items_schema = ItemSchema(many=True)