# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from authentication import auth_routes,init_auth  # Import routes from authentication.py
from event_creation import event_routes, init_events
from profile import profile_routes, init_profile
from event import event_routes, init_events
from invitation import invite_route, init_invitations
from profile import profile_routes
from pymongo import MongoClient
from recommendation import init_profile, recommendation_routes
import os
from dotenv import load_dotenv
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Connect to local MongoDB
db = client['invyta']  # Use or create a database named 'invyta'

# Pass the MongoDB connection to the authentication module
init_auth(db)
init_events(db)
init_profile(db)
init_invitations(db)
# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback_jwt_secret_key')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your_email@example.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your_email_password')

# Initialize extensions
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# Register authentication routes
app.register_blueprint(auth_routes)
app.register_blueprint(profile_routes)
app.register_blueprint(event_routes)
app.register_blueprint(recommendation_routes)
app.register_blueprint(invite_route)
# Run the application
if __name__ == '__main__':
    app.run(debug=True)