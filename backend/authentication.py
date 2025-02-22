# authentication.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pyotp

# Create a Blueprint for authentication routes
auth_routes = Blueprint('auth_routes', __name__)

# Initialize extensions (they will be initialized in app.py)
bcrypt = Bcrypt()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

# In-memory storage for demo purposes
users = {}
otp_storage = {}

@auth_routes.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users:
        return jsonify({"message": "User already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Store user
    users[email] = {'password': hashed_password, 'verified': False}

    # Generate OTP
    otp = pyotp.TOTP(pyotp.random_base32()).now()
    otp_storage[email] = otp

    # Send OTP via email
    msg = Message('Your OTP Code', sender='your_email@example.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}'
    mail.send(msg)

    return jsonify({"message": "User registered. Please verify your email."}), 201

@auth_routes.route('/verify', methods=['POST'])
@limiter.limit("5 per minute")
def verify():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if email not in users:
        return jsonify({"message": "User does not exist"}), 404

    if otp_storage.get(email) != otp:
        return jsonify({"message": "Invalid OTP"}), 400

    users[email]['verified'] = True
    del otp_storage[email]

    return jsonify({"message": "Email verified successfully"}), 200

@auth_routes.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email not in users or not bcrypt.check_password_hash(users[email]['password'], password):
        return jsonify({"message": "Invalid credentials"}), 401

    if not users[email]['verified']:
        return jsonify({"message": "Email not verified"}), 403

    # Create JWT token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@auth_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200