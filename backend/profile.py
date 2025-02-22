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

client = MongoClient('mongodb://localhost:27017/')  # Connect to local MongoDB
db = client['invyta']  # Use or create a database named 'auth_db'
users_collection = db['users']  # Use or create a collection named 'users'

profile_routes = Blueprint('profile_routes', __name__)

@profile_routes.route("/profile",methods=['POST'])
def update_data():  #update profile (user name, bio,)
    data = request.get_json()
    user_name = data.get("user_name")
    id = data.get("user_id")
    bio = data.get('bio')
    users_collection.update_one({"user_id":id},{"$set":{"username": user_name, "bio":bio}})
    return jsonify({"message": "User Updated."}), 201

