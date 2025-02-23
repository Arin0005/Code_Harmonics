
from pymongo import MongoClient
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# def init_profile(db):
#     global users_collection
#     users_collection = db['users']  # Use or create a collection named 'users'
client = MongoClient('mongodb://localhost:27017/')  # Connect to local MongoDB
db = client['invyta']
users_collection = db['users']

profile_routes = Blueprint('profile_routes', __name__)  # Use or create a collection named 'users'

@profile_routes.route("/profile", methods=['POST'])
@jwt_required()  # Require a valid JWT token to access this route
def update_data():
    # Get the current user's email from the JWT token
    current_user_email = get_jwt_identity()

    # Find the user in the database
    user = users_collection.find_one({"email": current_user_email})
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get the user_id from the user document
    user_id = user['user_id']

    # Get the updated profile data from the request
    data = request.get_json()
    username = data.get("username")
    bio = data.get("bio")
    favorite = str(data.get("favorite"))

    # Update the user's profile in the database
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"username": username, "bio": bio, "favorite": favorite.split(",")}}
    )

    return jsonify({"message": "User Updated."}), 201

@profile_routes.route("/profile", methods=['GET'])
@jwt_required()  # Require a valid JWT token
def get_profile():
    """
    Get the profile of the currently logged-in user.
    """
    # Get the user_id from the JWT token
    current_user_email = get_jwt_identity()

    # Fetch the user profile from the database
    response = users_collection.find_one(
        {"email": current_user_email},
        {"bio": 1, "_id": 0, "email": 1, "username": 1, "user_id": 1, "created_on": 1,"favorite": 1}
    )

    if not response:
        return jsonify({"message": "User not found"}), 404

    return jsonify(response), 200