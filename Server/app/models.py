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
