from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from .config import BaseConfig

from .machine import FeatureExtractor
fe = FeatureExtractor()

db = SQLAlchemy()
migrate = Migrate(compare_type=True)

def create_app():
    app = Flask(__name__)

    app.config.from_object(BaseConfig)
    api = Api(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

   

    from . import models

    from.home_controller import HomeKPI
    api.add_resource(HomeKPI, '/home')

    from .crawler import Crawl, MusinsaBrandCrawler
    api.add_resource(Crawl, '/crawl')
    api.add_resource(MusinsaBrandCrawler, '/crawl/brand/musinsa')

    from .keyword_controller import ItemList
    api.add_resource(ItemList, '/search')

    from .image_controller import ImageUpload, ImageSearch
    api.add_resource(ImageUpload, '/image/upload')
    api.add_resource(ImageSearch, '/search/image')

    return app