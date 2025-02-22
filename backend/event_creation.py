# events.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient

# Create a Blueprint for event routes
event_routes = Blueprint('event_routes', __name__)

# MongoDB collections (will be initialized later)
events_collection = None

def init_events(db):
    global events_collection
    events_collection = db['events']  # Use or create a collection named 'events'

@event_routes.route('/create', methods=['POST'])
def create_event():
    """
    Create a new event.
    """
    data = request.get_json()

    # Extract event details from the request
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')  # Expected format: "YYYY-MM-DD"
    backdrop_image = data.get('backdrop_image','')
    location = data.get('location')
    max_people = data.get('max_people')
    is_private = data.get('is_private', False)  # Default to False if not provided
    tags = data.get('tags')  # Default to empty list if not provided

    # Validate required fields
    if not all([user_id, title, description, date, location, max_people,tags]):
        return jsonify({"message": "Missing required fields"}), 400

    # Create event document
    event_data = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "schedule_date": datetime.strptime(date, "%Y-%m-%d"),  # Convert string to datetime object
        "backdrop_image": backdrop_image,
        "location": location,
        "max_people": max_people,
        "is_private": is_private,
        "tags": tags,
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