# events.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from flask_jwt_extended import jwt_required, get_jwt_identity
import secrets
from werkzeug.utils import secure_filename
from gridfs import GridFS
# Create a Blueprint for event routes
event_routes = Blueprint('event_routes', __name__)

# MongoDB collections (will be initialized later)
events_collection = None

def init_events(db):
    global events_collection, users_collection,fs
    events_collection = db['events']  # Use or create a collection named 'events'
    users_collection = db['users']
    fs = GridFS(db)

@event_routes.route('/create', methods=['POST'])
@jwt_required()  # Require a valid JWT token to access this route
def create_event():
    # Get the identity of the logged-in user from the JWT token
    current_user_email = get_jwt_identity()

    # Find the user in the database to get their user_id
    user = users_collection.find_one({"email": current_user_email})
    if not user:
        return jsonify({"message": "User not found"}), 404

    user_id = user['user_id']  # Extract the user_id from the user document

    data = request.get_json()

    # Extract event details from the request
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')  # Expected format: "YYYY-MM-DD"
    backdrop_image = data.get('backdrop_image')
    location = data.get('location')
    max_people = data.get('max_people')
    is_private = data.get('is_private', False)  # Default to False if not provided
    tags = data.get('tags', [])  # Default to empty list if not provided

    # Validate required fields
    if not all([title, description, date, location, max_people]):
        return jsonify({"message": "Missing required fields"}), 400

    # Create event document
    event_data = {
        "user_id": user_id,  # Use the user_id from the logged-in user
        "title": title,
        "description": description,
        "date": datetime.strptime(date, "%Y-%m-%d"),  # Convert string to datetime object
        "backdrop_image": backdrop_image,
        "location": location,
        "max_people": max_people,
        "is_private": is_private,
        "tags": tags,
        "media": [],
        "created_at": datetime.utcnow(),  # Store creation timestamp
        "updated_at": datetime.utcnow(),  # Store update timestamp
    }

    # Insert event into MongoDB
    result = events_collection.insert_one(event_data)

    # Return success response with event ID
    return jsonify({"message": "Event created successfully", "event_id": str(result.inserted_id)}), 201

@event_routes.route('/<event_id>', methods=['GET'])
def get_event(event_id):
    """
    Retrieve an event by its ID.
    """
    try:
        event = events_collection.find_one({"_id": ObjectId(event_id)})
        if not event:
            return jsonify({"message": "Event not found"}), 404

        # Convert ObjectId to string for JSON serialization
        event['_id'] = str(event['_id'])
        event['date'] = event['date'].strftime("%Y-%m-%d")  # Convert datetime to string
        return jsonify(event), 200
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

@event_routes.route('/<event_id>', methods=['PUT'])
def update_event(event_id):
    """
    Update an existing event.
    """
    data = request.get_json()

    # Validate event ID
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Prepare update data
    update_data = {}
    if 'title' in data:
        update_data['title'] = data['title']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'date' in data:
        update_data['date'] = datetime.strptime(data['date'], "%Y-%m-%d")
    if 'backdrop_image' in data:
        update_data['backdrop_image'] = data['backdrop_image']
    if 'location' in data:
        update_data['location'] = data['location']
    if 'max_people' in data:
        update_data['max_people'] = data['max_people']
    if 'is_private' in data:
        update_data['is_private'] = data['is_private']
    if 'tags' in data:
        update_data['tags'] = data['tags']

    # Add updated_at timestamp
    update_data['updated_at'] = datetime.utcnow()

    # Update event in MongoDB
    result = events_collection.update_one({"_id": event_id}, {"$set": update_data})

    if result.matched_count == 0:
        return jsonify({"message": "Event not found"}), 404

    return jsonify({"message": "Event updated successfully"}), 200

@event_routes.route('/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """
    Delete an event by its ID.
    """
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Delete event from MongoDB
    result = events_collection.delete_one({"_id": event_id})

    if result.deleted_count == 0:
        return jsonify({"message": "Event not found"}), 404

    return jsonify({"message": "Event deleted successfully"}), 200

@event_routes.route('/event/<user_id>', methods=['GET'])
def get_events_by_user(user_id):
    """
    Retrieve all events created by a specific user.
    """
    try:
        # Query MongoDB for events created by the user
        events = list(events_collection.find({"user_id": user_id}))

        # If no events are found, return a 404 response
        if not events:
            return jsonify({"message": "No events found for this user"}), 404

        # Convert MongoDB documents to a JSON-friendly format
        for event in events:
            event['_id'] = str(event['_id'])  # Convert ObjectId to string
            event['date'] = event['date'].strftime("%Y-%m-%d")  # Convert datetime to string
            event['created_at'] = event['created_at'].strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp
            event['updated_at'] = event['updated_at'].strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp

        # Return the list of events
        return jsonify(events), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@event_routes.route('/generate-invite-link/<event_id>', methods=['GET'])
@jwt_required()
def generate_invite_link(event_id):
    """
    Generate a unique invitation link for an event.
    """
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Check if the event exists
    event = events_collection.find_one({"_id": event_id})
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Generate a unique token for the invitation link
    token = secrets.token_urlsafe(16)  # Generates a secure, random token

    # Store the token in the event document (optional)
    events_collection.update_one(
        {"_id": event_id},
        {"$set": {"invite_token": token}}
    )

    # Generate the invitation link
    invite_link = f"https://yourapp.com/events/join?event_id={event_id}&token={token}"

    return jsonify({"invite_link": invite_link}), 200

@event_routes.route('/event/<event_id>/attendees', methods=['GET'])
def get_attendees(event_id):
    """
    Retrieve the list of attendees for an event.
    """
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Get the event document
    event = events_collection.find_one({"_id": event_id})
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Get the list of attendees
    attendees = event.get('attendees', [])

    return jsonify({"attendees": attendees}), 200

@event_routes.route('/events/<event_id>/media/upload', methods=['POST'])
@jwt_required()
def upload_media(event_id):
    """
    Upload a media file (photo/video) to an event and store it in GridFS.
    """
    # Validate event ID
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Check if the event exists
    event = events_collection.find_one({"_id": event_id})
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Get the current user's ID
    current_user_email = get_jwt_identity()
    user = users_collection.find_one({"email": current_user_email})
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_id = user['user_id']

    # Check if the user is an attendee
    if user_id not in event.get('attendees', []):
        return jsonify({"message": "You are not an attendee of this event"}), 403

    # Get the uploaded file
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400

    # Secure the filename
    filename = secure_filename(file.filename)

    # Store the file in GridFS
    try:
        file_id = fs.put(file, filename=filename, uploaded_by=user_id)
    except Exception as e:
        return jsonify({"message": "File upload failed", "error": str(e)}), 500

    # Add the media file to the event's media list
    media_entry = {
        "file_id": str(file_id),
        "uploaded_by": user_id,
        "status": "pending",  # Default status is pending
        "uploaded_at": datetime.utcnow(),
    }

    events_collection.update_one(
        {"_id": event_id},
        {"$push": {"media": media_entry}}
    )

    return jsonify({"message": "File uploaded successfully", "file_id": str(file_id)}), 200

@event_routes.route('/events/<event_id>/media/<file_id>', methods=['GET'])
def get_media(event_id, file_id):
    """
    Retrieve a media file from GridFS.
    """
    # Validate event ID
    try:
        event_id = ObjectId(event_id)
        file_id = ObjectId(file_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID or file ID"}), 400

    # Check if the event exists
    event = events_collection.find_one({"_id": event_id})
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Check if the file exists in the event's media list
    media_entry = next((media for media in event.get('media', []) if media['file_id'] == str(file_id)), None)
    if not media_entry:
        return jsonify({"message": "File not found in this event"}), 404

    # Fetch the file from GridFS
    try:
        file = fs.get(file_id)
        return file.read(), 200, {'Content-Type': file.content_type}
    except Exception as e:
        return jsonify({"message": "Failed to retrieve file", "error": str(e)}), 500
    
@event_routes.route('/events/<event_id>/media/moderate', methods=['POST'])
@jwt_required()
def moderate_media(event_id):
    """
    Approve or reject a media file for an event.
    """
    data = request.get_json()
    file_id = data.get('file_id')
    status = data.get('status')  # "approved" or "rejected"

    # Validate event ID
    try:
        event_id = ObjectId(event_id)
        file_id = ObjectId(file_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID or file ID"}), 400

    # Check if the event exists
    event = events_collection.find_one({"_id": event_id})
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Check if the current user is the event creator
    current_user_email = get_jwt_identity()
    user = users_collection.find_one({"email": current_user_email})
    if not user or user['user_id'] != event['user_id']:
        return jsonify({"message": "You are not authorized to moderate this event"}), 403

    # Update the media status
    result = events_collection.update_one(
        {"_id": event_id, "media.file_id": str(file_id)},
        {"$set": {"media.$.status": status}}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Media file not found"}), 404

    return jsonify({"message": f"Media file {status} successfully"}), 200

@event_routes.route('/events/<event_id>/media', methods=['GET'])
def list_media(event_id):
    """
    Retrieve all media files for an event.
    """
    # Validate event ID
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Check if the event exists
    event = events_collection.find_one({"_id": event_id})
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Return the list of media files
    media_files = event.get('media', [])
    return jsonify({"media": media_files}), 200