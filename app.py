import os
from flask import Flask,jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST
from db import db

import models
from flask_jwt_extended import JWTManager
def create_app(db_url=None):
    
    # dunder name as arguements
    app=Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate=Migrate(app,db)
    api=Api(app)
    #generate jwq secret key using the command secrets.SystemRandom().getrandbit(128)
    app.config["JWT_SECRET_KEY"]="jose"

    jwt=JWTManager(app)
    
    @jwt.needs_fresh_token_loader
    def token_not_refresh_callback(jwt_header,jwt_payload):
        return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return(jsonify(
            {"description":"The token has been revoked.","error":"token_revoked"}
        ),401)
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    # with app.app_context():
    #     #if tables already exists then table will not be created
    #     db.create_all()
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app



































# #POSTS
# #Add details about a store
# @app.post("/store")
# def create_store():
#     store_data=request.get_json()
#     if "name" not in store_data:
#         abort(400, message="Bad Request : name is required")
        
#     for store in stores:
#         if store["name"]==store_data["name"]:
#             abort(400, message="Bad Request : Store already exists")
            
#     store_id=uuid.uuid4().hex
#     store={**store_data,"id":store_id}
#     stores[store_id]=store
#     return store,201


# #Create items for the Store
# @app.post("/item")
# def create_item():
#     items_data=request.get_json()
#     if ("price" not in items_data or "store_id" not in items_data or "name" not in items_data):
#         abort(400, message="bad Request , Ensure all the required fields are passed while posting the data")
    
#     for item in items.values():
#         if item["store_id"]==items_data["store_id"] and item["name"]==items_data["name"]:
#             abort(400, message="Item already exists")
            
#     if items_data["store_id"] not in stores:
#         abort(404,message="Store not found")
        
#     item_id=uuid.uuid4().hex
#     item={**items_data,"id":item_id}
#     items[item_id]=item
#     return items,201

# #GET
# # Get details about a store
# @app.get("/store")
# def get_Stores():
#     return {"stores": list(stores.values())}

# # Get details about a store
# @app.get("/store/<string:store_id>")
# def get_items(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         abort(404,message="Store not found")

# #Get item details
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404,message="Item not found")
        
# #Get all items in a store
# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}


# #DELETE
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted successfully"},200
#     except KeyError:
#         abort(404,message="Item not found")

# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted successfully"},200
#     except KeyError:
#         abort(404,message="Store not found")
        

# #UPDATING
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     items_data=request.get_json()
#     if ("price" not in items_data or "store_id" not in items_data or "name" not in items_data):
#         abort(400, message="bad Request , Ensure all the required fields are passed while posting the data")
#     try:
#         item=items[item_id]
#         #***This line will automatically updates the item with the new data according to the item id****
#         item |=items_data        
#         return item
#     except KeyError:
#         abort(404,message="Item not Found")
#         {"message":"Items are updated"},202
        