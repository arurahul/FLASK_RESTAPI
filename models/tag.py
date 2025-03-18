from db import db

class TagModel(db.Model):
    __tablename__="tags"
    
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(80),nullable=False,unique=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    #One to many relationship with store
    store = db.relationship("StoreModel", back_populates="tags")
    
    #Many to Many relationship with items , also include the secondary table which contains the relationship details.
    items=db.relationship("ItemModel",back_populates="tags",secondary="item_tags")