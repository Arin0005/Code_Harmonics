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

recommendation_routes = Blueprint('recommendation_routes', __name__)

client = MongoClient('mongodb://localhost:27017/')  # Connect to local MongoDB
db = client['invyta']
users_collection = db['users']
events_collection = db['events']

@recommendation_routes.route("/recommend", methods=['GET'])
@jwt_required() 
def recommend():
    try:
        current_user_email = get_jwt_identity()
        user = users_collection.find_one({"email":current_user_email })
        if not user:
            return jsonify({"error": "User not found"}), 404

        favorites = user.get("favorite", [])
        if not favorites:
            return jsonify({"message": "No favorites found. Add some to get recommendations!"})

        # Find events that match the user's favorite categories
        recommended_events = events_collection.find({"tags": {"$in": favorites}})

        events_list = []
        for event in recommended_events:
            event["_id"] = str(event["_id"])  # Convert ObjectId to string
            events_list.append(event)

        return jsonify({"recommended_events": events_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



