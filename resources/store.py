import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from schemas import StoreSchema
from models import StoreModel
blp=Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store
            
    def delete(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted"},200

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores=StoreModel.query.all()
        return stores

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self,store_data):
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
            
        except IntegrityError:
            abort(400, message="An error occurred while inserting the store details.")
        except SQLAlchemyError:
            abort(500, message="Error occurred while creating store")
        return store,201
