# Event Management API

This is a Flask-based API for managing events, user authentication, profiles, and event recommendations. It uses MongoDB as the database and includes features like JWT authentication, email verification, rate limiting, and QR code generation for event invitations.

---

## Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup and Installation](#setup-and-installation)
4. [API Endpoints](#api-endpoints)
5. [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features
- **User Authentication**: Register, login, and email verification with OTP.
- **Event Management**: Create, update, and list events.
- **Profile Management**: Update user profiles.
- **Event Recommendations**: Get personalized event recommendations.
- **Event Joining**: Join events and generate QR codes for invitations.
- **Rate Limiting**: Prevent abuse with rate limiting.
- **Email Notifications**: Send emails for OTP and event invitations.

---

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt
- **Email**: Flask-Mail
- **Rate Limiting**: Flask-Limiter
- **File Storage**: GridFS (for large files)
- **Environment Management**: `python-dotenv`
- **CORS**: Flask-CORS

---

## Setup and Installation

### Prerequisites
- Python 3.x
- MongoDB (running locally or remotely)
- SMTP server (e.g., Gmail for sending emails)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/event-management-api.git
   cd event-management-api


   1. Imports and Initialization
Imports:

uuid: Generates unique user IDs.

datetime: Tracks the creation date of user accounts.

flask: Core Flask functionality for routing and request handling.

flask_jwt_extended: Manages JSON Web Tokens (JWT) for secure authentication.

flask_bcrypt: Hashes passwords for secure storage.

flask_mail: Sends emails (e.g., OTP for email verification).

flask_limiter: Limits the number of requests to prevent abuse.

pyotp: Generates One-Time Passwords (OTP) for email verification.

pymongo: Interacts with MongoDB for database operations.

Blueprint:

auth_routes = Blueprint('auth_routes', __name__): Creates a Flask Blueprint to organize authentication-related routes.

Extensions:

bcrypt = Bcrypt(): Initializes Bcrypt for password hashing.

mail = Mail(): Initializes Flask-Mail for sending emails.

limiter = Limiter(key_func=get_remote_address): Initializes Flask-Limiter to limit requests based on the client's IP address.

2. Database Initialization
init_auth(db):

Initializes the MongoDB collections (users and otps) for storing user data and OTPs.

users_collection: Stores user details like email, password, and verification status.

otp_collection: Stores OTPs for email verification.

3. Registration Route (/register)
Purpose: Registers a new user.

Steps:

Extracts email and password from the request.

Checks if the user already exists in the database.

Hashes the password using Bcrypt.

Creates a new user document with default values (e.g., user_id, verified, created_on).

Generates an OTP using pyotp.

Stores the OTP in the otp_collection.

Sends the OTP to the user's email using Flask-Mail.

Returns a success message.

4. Email Verification Route (/verify)
Purpose: Verifies the user's email using the OTP.

Steps:

Extracts email and otp from the request.

Checks if the user exists in the database.

Validates the OTP by comparing it with the stored OTP.

Marks the user as verified in the users_collection.

Deletes the OTP from the otp_collection.

Returns a success message.

5. Login Route (/login)
Purpose: Authenticates a user and issues a JWT token.

Steps:

Extracts email and password from the request.

Checks if the user exists and if the password is correct using Bcrypt.

Verifies if the user's email is verified.

Generates a JWT token using create_access_token.

Returns the JWT token, user ID, and a flag indicating whether the user has a username.

6. Protected Route (/protected)
Purpose: Demonstrates a protected route that requires a valid JWT token.

Steps:

Uses @jwt_required() to enforce JWT authentication.

Retrieves the current user's identity from the JWT token.

Returns the logged-in user's email.

README.md
markdown
Copy
# Authentication API

This API provides user authentication functionality, including registration, email verification, and login. It uses Flask, MongoDB, and several Flask extensions to ensure security and efficiency.

---

## **Features**
1. **User Registration**:
   - Users can register with an email and password.
   - Passwords are hashed using Bcrypt for secure storage.
   - An OTP is generated and sent to the user's email for verification.

2. **Email Verification**:
   - Users must verify their email using the OTP sent to them.
   - Once verified, the user's account is marked as verified.

3. **User Login**:
   - Users can log in with their email and password.
   - A JWT token is issued upon successful login.
   - The token is required to access protected routes.

4. **Rate Limiting**:
   - Limits the number of requests to prevent abuse (e.g., 5 requests per minute for registration, verification, and login).

5. **Protected Routes**:
   - Demonstrates how to protect routes using JWT authentication.

---

## **Endpoints**

### **1. Register**
- **URL**: `/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
Response:

json
Copy
{
  "message": "User registered. Please verify your email."
}
2. Verify Email
URL: /verify

Method: POST

Request Body:

json
Copy
{
  "email": "user@example.com",
  "otp": "123456"
}
Response:

json
Copy
{
  "message": "Email verified successfully"
}
3. Login
URL: /login

Method: POST

Request Body:

json
Copy
{
  "email": "user@example.com",
  "password": "securepassword"
}
Response:

json
Copy
{
  "access_token": "jwt_token",
  "has_username": false,
  "user_id": "abc123"
}
4. Protected Route
URL: /protected

Method: GET

Headers:

json
Copy
{
  "Authorization": "Bearer <jwt_token>"
}
Response:

json
Copy
{
  "logged_in_as": "user@example.com"
}
Setup
Install dependencies:

bash
Copy
pip install Flask flask-jwt-extended flask-bcrypt flask-mail flask-limiter pyotp pymongo
Configure Flask-Mail with your email provider's SMTP settings.

Initialize the MongoDB database and collections:

python
Copy
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['auth_db']
Run the Flask application:

bash
Copy
flask run
Dependencies
Flask

Flask-JWT-Extended

Flask-Bcrypt

Flask-Mail

Flask-Limiter

PyOTP

PyMongo

Rate Limiting
Registration, verification, and login endpoints are limited to 5 requests per minute per user.

Security
Passwords are hashed using Bcrypt.

JWT tokens are used for secure authentication.

OTPs are used for email verification.

1. Imports and Initialization
Imports:

flask: Core Flask functionality for routing and request handling.

datetime: Tracks the creation date of events.

bson.ObjectId: Validates and converts MongoDB ObjectIDs.

pymongo: Interacts with MongoDB for database operations.

flask_jwt_extended: Manages JSON Web Tokens (JWT) for secure authentication.

secrets: Generates secure tokens for event invitations.

Blueprint:

event_join_routes = Blueprint('event_join_routes', __name__): Creates a Flask Blueprint to organize event-related routes.

Database Collections:

events_collection: Stores event details like attendees, invite tokens, and RSVP statuses.

users_collection: Stores user details like email and user ID.

2. Database Initialization
init_event_join(db):

Initializes the MongoDB collections (events and users) for storing event and user data.

3. Join Event Route (/join)
Purpose: Allows a user to join an event using an invitation link.

Steps:

Extracts event_id and token from the request.

Validates the event_id using ObjectId.

Retrieves the current user's email from the JWT token and fetches the user's ID from the database.

Checks if the event exists and if the invitation token is valid.

Handles public and private events:

For private events, adds the user to the pending_approval list.

For public events, adds the user directly to the attendees list.

Returns a success message.

4. Update RSVP Status Route (/event/<event_id>/rsvp)
Purpose: Updates a user's RSVP status for an event.

Steps:

Extracts rsvp_status from the request (valid values: attending, not_attending, maybe).

Validates the event_id using ObjectId.

Retrieves the current user's email from the JWT token and fetches the user's ID from the database.

Checks if the event exists.

Updates the user's RSVP status in the event's attendees list.

Returns a success message.

README.md
markdown
Copy
# Event Join API

This API provides functionality for joining events and updating RSVP statuses. It uses Flask, MongoDB, and JWT for secure authentication and data storage.

---

## **Features**
1. **Join Event**:
   - Users can join an event using an invitation link.
   - Handles both public and private events:
     - Public events: Users are added directly to the attendees list.
     - Private events: Users are added to the pending approval list.

2. **Update RSVP Status**:
   - Users can update their RSVP status for an event (`attending`, `not_attending`, `maybe`).

3. **Authentication**:
   - All routes require a valid JWT token for access.

---

## **Endpoints**

### **1. Join Event**
- **URL**: `/join`
- **Method**: `POST`
- **Headers**:
  ```json
  {
    "Authorization": "Bearer <jwt_token>"
  }
Request Body:

json
Copy
{
  "event_id": "64f8a1b2c9b5f3a1c8f7e6d5",
  "token": "invitation_token"
}
Response:

For public events:

json
Copy
{
  "message": "Successfully joined the event"
}
For private events:

json
Copy
{
  "message": "Your request to join the event is pending approval"
}
2. Update RSVP Status
URL: /event/<event_id>/rsvp

Method: POST

Headers:

json
Copy
{
  "Authorization": "Bearer <jwt_token>"
}
Request Body:

json
Copy
{
  "rsvp_status": "attending"
}
Response:

json
Copy
{
  "message": "RSVP status updated successfully"
}
Setup
Install dependencies:

bash
Copy
pip install Flask flask-jwt-extended pymongo
Initialize the MongoDB database and collections:

python
Copy
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['event_db']
Run the Flask application:

bash
Copy
flask run
Dependencies
Flask

Flask-JWT-Extended

PyMongo

Authentication
All routes require a valid JWT token for access.

The token is obtained during user login and must be included in the Authorization header.

Database Schema
Events Collection
json
Copy
{
  "_id": ObjectId,
  "name": String,
  "description": String,
  "is_private": Boolean,
  "invite_token": String,
  "attendees": [String],  // List of user IDs
  "pending_approval": [String],  // List of user IDs (for private events)
  "rsvp_status": {
    "user_id": String,  // User ID
    "status": String  // "attending", "not_attending", "maybe"
  }
}
Users Collection
json
Copy
{
  "_id": ObjectId,
  "user_id": String,
  "email": String,
  "password": String,
  "verified": Boolean
}


1. Imports and Initialization
Imports:

flask: Core Flask functionality for routing and request handling.

datetime: Tracks the creation and update timestamps of events.

bson.ObjectId: Validates and converts MongoDB ObjectIDs.

pymongo: Interacts with MongoDB for database operations.

flask_jwt_extended: Manages JSON Web Tokens (JWT) for secure authentication.

secrets: Generates secure tokens for event invitations.

qrcode: Generates QR codes for event invitation links.

io: Handles in-memory binary data (e.g., QR code images).

werkzeug.utils.secure_filename: Secures filenames for uploaded media.

gridfs.GridFS: Stores and retrieves large files (e.g., media) in MongoDB.

Blueprint:

event_routes = Blueprint('event_routes', __name__): Creates a Flask Blueprint to organize event-related routes.

Database Collections:

events_collection: Stores event details like title, description, attendees, and media.

users_collection: Stores user details like email and user ID.

fs: Initializes GridFS for storing large files (e.g., media).

2. Database Initialization
init_events(db):

Initializes the MongoDB collections (events and users) and GridFS for storing event and user data.

3. Create Event Route (/create)
Purpose: Allows a user to create a new event.

Steps:

Retrieves the current user's email from the JWT token and fetches the user's ID from the database.

Extracts event details (e.g., title, description, date) from the request.

Validates required fields.

Creates an event document and inserts it into the events_collection.

Returns a success response with the event ID.

4. Get Event Route (/<event_id>)
Purpose: Retrieves an event by its ID.

Steps:

Validates the event_id using ObjectId.

Fetches the event from the events_collection.

Converts the event document to a JSON-friendly format (e.g., converting ObjectId to string).

Returns the event details.

5. Update Event Route (/<event_id>)
Purpose: Updates an existing event.

Steps:

Validates the event_id using ObjectId.

Extracts update data from the request.

Updates the event document in the events_collection.

Returns a success message.

6. Delete Event Route (/<event_id>)
Purpose: Deletes an event by its ID.

Steps:

Validates the event_id using ObjectId.

Deletes the event from the events_collection.

Returns a success message.

7. Get Events by User Route (/event/<user_id>)
Purpose: Retrieves all events created by a specific user.

Steps:

Fetches all events from the events_collection where user_id matches.

Converts the event documents to a JSON-friendly format.

Returns the list of events.

8. Generate Invitation Link Route (/generate-invite-link/<event_id>)
Purpose: Generates a unique invitation link for an event.

Steps:

Validates the event_id using ObjectId.

Generates a secure token using secrets.

Stores the token in the event document.

Generates and returns the invitation link.

9. Get Attendees Route (/event/<event_id>/attendees)
Purpose: Retrieves the list of attendees for an event.

Steps:

Validates the event_id using ObjectId.

Fetches the event document and retrieves the list of attendees.

Returns the list of attendees.

10. Upload Media Route (/events/<event_id>/media/upload)
Purpose: Uploads a media file (photo/video) to an event and stores it in GridFS.

Steps:

Validates the event_id using ObjectId.

Checks if the user is an attendee of the event.

Secures the filename and stores the file in GridFS.

Adds the media file to the event's media list.

Returns a success message with the file ID.

11. Get Media Route (/events/<event_id>/media/<file_id>)
Purpose: Retrieves a media file from GridFS.

Steps:

Validates the event_id and file_id using ObjectId.

Fetches the file from GridFS.

Returns the file as a response.

12. Moderate Media Route (/events/<event_id>/media/moderate)
Purpose: Approves or rejects a media file for an event.

Steps:

Validates the event_id and file_id using ObjectId.

Checks if the current user is the event creator.

Updates the media file's status in the event document.

Returns a success message.

13. List Media Route (/events/<event_id>/media)
Purpose: Retrieves all media files for an event.

Steps:

Validates the event_id using ObjectId.

Fetches the event document and retrieves the list of media files.

Returns the list of media files.

14. Generate QR Code Route (/generate-qr-code/<event_id>)
Purpose: Generates a QR code for the event's invitation link.

Steps:

Validates the event_id using ObjectId.

Fetches the event's invitation link.

Generates a QR code for the invitation link.

Returns the QR code image as a response.

README.md
markdown
Copy
# Event Management API

This API provides functionality for managing events, including creating, retrieving, updating, and deleting events. It also supports features like generating invitation links, uploading and moderating media, and generating QR codes.

---

## **Features**
1. **Create Event**:
   - Users can create events with details like title, description, date, and location.
   - Events can be marked as private or public.

2. **Retrieve Event**:
   - Fetch event details by event ID.

3. **Update Event**:
   - Update event details like title, description, and location.

4. **Delete Event**:
   - Delete an event by its ID.

5. **Generate Invitation Link**:
   - Generate a unique invitation link for an event.

6. **Upload Media**:
   - Upload media files (photos/videos) to an event.
   - Media files are stored in GridFS.

7. **Moderate Media**:
   - Approve or reject media files uploaded by attendees.

8. **Generate QR Code**:
   - Generate a QR code for the event's invitation link.

---

## **Endpoints**

### **1. Create Event**
- **URL**: `/create`
- **Method**: `POST`
- **Headers**:
  ```json
  {
    "Authorization": "Bearer <jwt_token>"
  }
Request Body:

json
Copy
{
  "title": "Event Title",
  "description": "Event Description",
  "date": "2023-12-31",
  "location": "Event Location",
  "max_people": 100,
  "is_private": false,
  "tags": ["tech", "conference"]
}
Response:

json
Copy
{
  "message": "Event created successfully",
  "event_id": "64f8a1b2c9b5f3a1c8f7e6d5"
}
2. Get Event
URL: /<event_id>

Method: GET

Response:

json
Copy
{
  "_id": "64f8a1b2c9b5f3a1c8f7e6d5",
  "title": "Event Title",
  "description": "Event Description",
  "date": "2023-12-31",
  "location": "Event Location",
  "max_people": 100,
  "is_private": false,
  "tags": ["tech", "conference"],
  "created_at": "2023-10-01 12:00:00",
  "updated_at": "2023-10-01 12:00:00"
}
3. Update Event
URL: /<event_id>

Method: PUT

Request Body:

json
Copy
{
  "title": "Updated Event Title",
  "description": "Updated Event Description"
}
Response:

json
Copy
{
  "message": "Event updated successfully"
}
4. Delete Event
URL: /<event_id>

Method: DELETE

Response:

json
Copy
{
  "message": "Event deleted successfully"
}
5. Generate Invitation Link
URL: /generate-invite-link/<event_id>

Method: GET

Response:

json
Copy
{
  "invite_link": "https://yourapp.com/events/join?event_id=64f8a1b2c9b5f3a1c8f7e6d5&token=invitation_token"
}
6. Upload Media
URL: /events/<event_id>/media/upload

Method: POST

Request Body:

Form-data with a file field named file.

Response:

json
Copy
{
  "message": "File uploaded successfully",
  "file_id": "64f8a1b2c9b5f3a1c8f7e6d5"
}
7. Generate QR Code
URL: /generate-qr-code/<event_id>

Method: GET

Response:

Returns a PNG image of the QR code.

Setup
Install dependencies:

bash
Copy
pip install Flask flask-jwt-extended pymongo qrcode gridfs
Initialize the MongoDB database and collections:

python
Copy
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['event_db']
Run the Flask application:

bash
Copy
flask run
Dependencies
Flask

Flask-JWT-Extended

PyMongo

qrcode

gridfs

Authentication
All routes (except /get_event) require a valid JWT token for access.

The token is obtained during user login and must be included in the Authorization header.


1. Imports and Initialization
Imports:

pymongo.MongoClient: Connects to the MongoDB database.

flask: Core Flask functionality for routing and request handling.

flask_jwt_extended: Manages JSON Web Tokens (JWT) for secure authentication.

Database Connection:

client = MongoClient('mongodb://localhost:27017/'): Connects to a local MongoDB instance.

db = client['invyta']: Uses or creates a database named invyta.

users_collection = db['users']: Uses or creates a collection named users.

Blueprint:

profile_routes = Blueprint('profile_routes', __name__): Creates a Flask Blueprint to organize profile-related routes.

2. Update Profile Route (/profile)
Purpose: Allows a user to update their profile information (e.g., username, bio, favorites).

Steps:

Retrieves the current user's email from the JWT token.

Fetches the user document from the users_collection using the email.

Extracts the user_id from the user document.

Extracts updated profile data (e.g., username, bio, favorite) from the request.

Updates the user's profile in the users_collection.

Returns a success message.

3. Get Profile Route (/get_profile/<string:user_id>)
Purpose: Retrieves a user's profile by their user_id.

Steps:

Extracts the user_id from the URL.

Fetches the user document from the users_collection using the user_id.

Returns the user's profile data (e.g., bio, email, username, user_id, created_on).

README.md
markdown
Copy
# Profile Management API

This API provides functionality for managing user profiles, including updating profile information and retrieving profile data. It uses Flask, MongoDB, and JWT for secure authentication and data storage.

---

## **Features**
1. **Update Profile**:
   - Users can update their profile information (e.g., username, bio, favorites).

2. **Get Profile**:
   - Retrieve a user's profile by their `user_id`.

---

## **Endpoints**

### **1. Update Profile**
- **URL**: `/profile`
- **Method**: `POST`
- **Headers**:
  ```json
  {
    "Authorization": "Bearer <jwt_token>"
  }
Request Body:

json
Copy
{
  "username": "new_username",
  "bio": "New bio",
  "favorite": ["hiking", "reading"]
}
Response:

json
Copy
{
  "message": "User Updated."
}
2. Get Profile
URL: /get_profile/<user_id>

Method: GET

Response:

json
Copy
{
  "username": "user123",
  "bio": "I love coding!",
  "email": "user@example.com",
  "user_id": "abc123",
  "created_on": "2023-10-01"
}
Setup
Install dependencies:

bash
Copy
pip install Flask flask-jwt-extended pymongo
Initialize the MongoDB database and collections:

python
Copy
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['invyta']
users_collection = db['users']
Run the Flask application:

bash
Copy
flask run
Dependencies
Flask

Flask-JWT-Extended

PyMongo

Authentication
The /profile route requires a valid JWT token for access.

The token is obtained during user login and must be included in the Authorization header.

Database Schema
Users Collection
json
Copy
{
  "_id": ObjectId,
  "user_id": String,
  "email": String,
  "username": String,
  "bio": String,
  "favorite": [String],
  "created_on": String
}

1. Imports and Initialization
Imports:

uuid: Generates unique identifiers (not used in this specific route but included for potential future use).

datetime: Tracks timestamps (not used in this specific route but included for potential future use).

flask: Core Flask functionality for routing and request handling.

flask_jwt_extended: Manages JSON Web Tokens (JWT) for secure authentication.

flask_bcrypt: Hashes passwords (not used in this specific route but included for potential future use).

flask_mail: Sends emails (not used in this specific route but included for potential future use).

flask_limiter: Limits the number of requests (not used in this specific route but included for potential future use).

pyotp: Generates One-Time Passwords (OTP) (not used in this specific route but included for potential future use).

pymongo: Interacts with MongoDB for database operations.

Blueprint:

recommendation_routes = Blueprint('recommendation_routes', __name__): Creates a Flask Blueprint to organize recommendation-related routes.

Database Initialization:

init_profile(db): Initializes the MongoDB collections (users and events) for storing user and event data.

2. Recommend Events Route (/recommend/<string:user_id>)
Purpose: Recommends events to a user based on their favorite categories.

Steps:

Retrieves the user's document from the users_collection using the user_id.

Checks if the user exists. If not, returns a 404 error.

Retrieves the user's favorite categories from the favorates field.

If no favorites are found, returns a message suggesting the user add favorites.

Queries the events_collection for events that match the user's favorite categories using the $in operator.

Converts the MongoDB ObjectId to a string for JSON serialization.

Returns a list of recommended events.

README.md
markdown
Copy
# Event Recommendation API

This API provides functionality for recommending events to users based on their favorite categories. It uses Flask and MongoDB for data storage and retrieval.

---

## **Features**
1. **Event Recommendations**:
   - Recommends events to users based on their favorite categories.

---

## **Endpoints**

### **1. Recommend Events**
- **URL**: `/recommend/<user_id>`
- **Method**: `GET`
- **Response**:
  - If the user has favorites:
    ```json
    {
      "recommended_events": [
        {
          "_id": "64f8a1b2c9b5f3a1c8f7e6d5",
          "title": "Tech Conference",
          "description": "A conference on the latest in tech.",
          "date": "2023-12-31",
          "location": "San Francisco",
          "tags": ["tech", "conference"]
        }
      ]
    }
    ```
  - If the user has no favorites:
    ```json
    {
      "message": "No favorites found. Add some to get recommendations!"
    }
    ```

---

## **Setup**
1. Install dependencies:
   ```bash
   pip install Flask flask-jwt-extended pymongo
Initialize the MongoDB database and collections:

python
Copy
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['invyta']
users_collection = db['users']
events_collection = db['events']
Run the Flask application:

bash
Copy
flask run
Dependencies
Flask

Flask-JWT-Extended

PyMongo

Database Schema
Users Collection
json
Copy
{
  "_id": ObjectId,
  "user_id": String,
  "email": String,
  "favorates": [String]  // List of favorite categories
}
Events Collection
json
Copy
{
  "_id": ObjectId,
  "title": String,
  "description": String,
  "date": String,
  "location": String,
  "tags": [String]  // List of event categories
}
How It Works
The /recommend/<user_id> endpoint retrieves the user's favorite categories from the users_collection.

It queries the events_collection for events that match any of the user's favorite categories.

The matching events are returned as recommendations.

License
This project is licensed under the MIT License.

Copy

---

### **How to Use**
1. Start the Flask application.
2. Use the `/recommend/<user_id>` endpoint to get event recommendations for a user.

This setup provides a simple and effective system for recommending events to users based on their preferences.
