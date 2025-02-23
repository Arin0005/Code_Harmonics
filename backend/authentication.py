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
# Create a Blueprint for authentication routes
#
auth_routes = Blueprint('auth_routes', __name__)

# Initialize extensions (they will be initialized in app.py)
bcrypt = Bcrypt()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

def init_auth(db):
    global users_collection, otp_collection
    users_collection = db['users']  # Use or create a collection named 'users'
    otp_collection = db['otps']

@auth_routes.route('/register', methods=['POST'])
@limiter.limit("5 per minute",key_func=lambda: request.get_json().get('email'))
def register():
    user_id_gen = lambda: uuid.uuid4().hex[:12]
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Check if user already exists
    if users_collection.find_one({'email': email}):
        return jsonify({"message": "User already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    docs = {
        'username': "",
        'user_id': user_id_gen(),
        'email': email,
        'password': hashed_password,
        'verified': False,
        "profile_pic": "",
        "created_on": datetime.today().strftime("%d/%m/%Y"),
        "favorites": [],
        "bio": "tell me about yourself!",
    }
    # Store user in MongoDB
    users_collection.insert_one(docs)

    # Generate OTP
    otp = pyotp.TOTP(pyotp.random_base32()).now()

    # Store OTP in MongoDB
    otp_collection.insert_one({
        'email': email,
        'otp': otp
    })

    # Send OTP via email
    msg = Message('Your OTP Code', sender='your_email@example.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}'
    mail.send(msg)

    return jsonify({"message": "User registered. Please verify your email."}), 201



@auth_routes.route('/verify', methods=['POST'])
@limiter.limit("5 per minute",key_func=lambda: request.get_json().get('email'))
def verify():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    # Check if user exists
    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({"message": "User does not exist"}), 404

    # Check if OTP is valid
    stored_otp = otp_collection.find_one({'email': email})
    if not stored_otp or stored_otp['otp'] != otp:
        return jsonify({"message": "Invalid OTP"}), 400

    # Mark user as verified
    users_collection.update_one({'email': email}, {'$set': {'verified': True}})

    # Delete OTP from MongoDB
    otp_collection.delete_one({'email': email})

    return jsonify({"message": "Email verified successfully"}), 200

@auth_routes.route('/login', methods=['POST'])
@limiter.limit("5 per minute",key_func=lambda: request.get_json().get('email'))
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if password is None:
        print("flag")

    user = users_collection.find_one({'email': email})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Check if email is verified
    if not user['verified']:
        return jsonify({"message": "Email not verified"}), 403

    if 'username' in user and user['username'] == "":
        has_username = False
    else:
        has_username = True

    # Create JWT token
    access_token = create_access_token(identity=email)
    return jsonify({
        "access_token": access_token,
        "has_username": has_username,
        "user_id": user['user_id'],
    }), 200
@auth_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200