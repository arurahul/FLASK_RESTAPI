from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),nullable=False,unique=False)
    description=db.Column(db.String())
    price=db.Column(db.Float(precision=2),nullable=False,unique=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    #One to many relationship with store
    store = db.relationship("StoreModel", back_populates="items")
    #Many to Many relationship with tags, also include the secondary table which contains the relationship details.
    tags=db.relationship("TagModel",back_populates="items",secondary="item_tags")

