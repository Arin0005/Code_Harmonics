
from pymongo import MongoClient
from flask import Blueprint, request, jsonify

# def init_profile(db):
#     global users_collection
#     users_collection = db['users']  # Use or create a collection named 'users'
client = MongoClient('mongodb://localhost:27017/')  # Connect to local MongoDB
db = client['invyta']
users_collection = db['users']

profile_routes = Blueprint('profile_routes', __name__)  # Use or create a collection named 'users'

@profile_routes.route("/profile",methods=['POST'])
def update_data():  #update profile (user name, bio,)
    data = request.get_json()
    # if "user_name" or "user_id" or "bio" or "favorates" not in data:
    #     return jsonify({"message": "incomplete request."}), 400

    username = data.get("username")
    id = data.get("user_id")
    bio = data.get("bio")
    favorite = data.get("favorite")
    users_collection.update_one({"user_id":id},{"$set":{"username": username, "bio":bio, "favorite": favorite}})
    return jsonify({"message": "User Updated."}), 201

@profile_routes.route("/get_profile/<string:user_id>",methods=['GET'])
def get_profile(user_id):
    id = user_id
    response = users_collection.find_one({"user_id":id},{"bio": 1,"_id":0,"email":1,"username":1,"user_id":1,"created_on":1})
    return response, 200