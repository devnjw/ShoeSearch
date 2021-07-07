from app import db

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(45))
    image_url = db.Column(db.String(255))
    item_url = db.Column(db.String(255))
    shop = db.Column(db.String(45))
    price = db.Column(db.String(45))
    brand = db.Column(db.String(45))

class Brand(db.Model):
    __tablename__ = "brand"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eng_name = db.Column(db.String(45))
    subs = db.Column(db.String(255))

class KPI(db.Model):
    __tablename__ = "KPI"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    visit = db.Column(db.Integer)
    string_search = db.Column(db.Integer)
    image_search = db.Column(db.Integer)

class SearchKeywords(db.Model):
    __tablename__ = "search_keyword"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String(45))
    cnt = db.Column(db.Integer)
    date = db.Column(db.Date, nullable=False)

class SearchImages(db.Model):
    __tablename__ = "search_image"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
