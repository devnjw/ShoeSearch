from PIL import Image
import numpy as np
import uuid
import os

from sqlalchemy.sql.expression import case

from app import fe, max_item_num

from app.models import SearchImages
from ..serializer import searched_images_schema

def get_searched_images():
    output = SearchImages.query.order_by(SearchImages.id.desc()).limit(max_item_num).all()
    output = searched_images_schema.dump(output)

    return output
