# authentication.py
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pyotp
from pymongo import MongoClient

def init_profile(db):
    global users_collection
    users_collection = db['users']  # Use or create a collection named 'users'

profile_routes = Blueprint('profile_routes', __name__)

@profile_routes.route("/profile",methods=['POST'])
def update_data():  #update profile (user name, bio,)
    data = request.get_json()
    # if "user_name" or "user_id" or "bio" or "favorates" not in data:
    #     return jsonify({"message": "incomplete request."}), 400

    user_name = data.get("user_name")
    id = data.get("user_id")
    bio = data.get("bio")
    favorates = data.get("favorates")
    users_collection.update_one({"user_id":id},{"$set":{"username": user_name, "bio":bio, "favorates": favorates}})
    return jsonify({"message": "User Updated."}), 201

