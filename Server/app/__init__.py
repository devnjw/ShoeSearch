from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from .config import BaseConfig

from .machine import FeatureExtractor
fe = FeatureExtractor()

db = SQLAlchemy()
migrate = Migrate(compare_type=True)

max_item_num = 96

def create_app():
    app = Flask(__name__)

    app.config.from_object(BaseConfig)
    api = Api(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)


    from . import models

    from .controller.home_controller import HomeKPI, PopularItems, PopularBrands
    api.add_resource(HomeKPI, '/home')
    api.add_resource(PopularItems, '/home/popular/items')
    api.add_resource(PopularBrands, '/home/popular/brands')

    from .crawler import MusinsaItemCrawler, MusinsaBrandCrawler, MusinsaItemWithCategoryCrawler
    api.add_resource(MusinsaItemCrawler, '/crawl/item/musinsa')
    api.add_resource(MusinsaBrandCrawler, '/crawl/brand/musinsa')
    api.add_resource(MusinsaItemWithCategoryCrawler, '/crawl/category/musinsa')

    from .controller.keyword_controller import KeywordSearch
    api.add_resource(KeywordSearch, '/search')

    from .controller.image_controller import ImageSearch
    api.add_resource(ImageSearch, '/search/image')

    from .controller.admin_controller import AdminImage
    api.add_resource(AdminImage, '/admin/image')

    return app