from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from flask_jwt_extended import jwt_required, get_jwt_identity
import secrets

# Create a Blueprint for event routes
event_join_routes = Blueprint('event_join_routes', __name__)

# MongoDB collections (will be initialized later)
events_collection = None
users_collection = None

def init_events(db):
    global events_collection, users_collection
    events_collection = db['events']  # Use or create a collection named 'events'
    users_collection = db['users']

@event_join_routes.route('/join', methods=['POST'])
@jwt_required()
def join_event():
    """
    Allow a user to join an event using an invitation link.
    """
    data = request.get_json()
    event_id = data.get('event_id')
    token = data.get('token')

    # Validate event ID
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Get the current user's ID from the JWT token
    current_user_email = get_jwt_identity()
    user = users_collection.find_one({"email": current_user_email})
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_id = user['user_id']

    # Check if the event exists and the token is valid
    event = events_collection.find_one({"_id": event_id, "invite_token": token})
    if not event:
        return jsonify({"message": "Invalid event ID or token"}), 400

    # Check if the user is already an attendee
    if user_id in event.get('attendees', []):
        return jsonify({"message": "You are already attending this event"}), 400

    # Handle public vs private events
    if event.get('is_private', False):
        # For private events, add the user to the "pending_approval" list
        events_collection.update_one(
            {"_id": event_id},
            {"$addToSet": {"pending_approval": user_id}}  # Prevent duplicates
        )
        return jsonify({"message": "Your request to join the event is pending approval"}), 200
    else:
        # For public events, add the user directly to the attendees list
        events_collection.update_one(
            {"_id": event_id},
            {"$addToSet": {"attendees": user_id}}  # Prevent duplicates
        )
        return jsonify({"message": "Successfully joined the event"}), 200
    
@event_join_routes.route('/event/<event_id>/rsvp', methods=['POST'])
@jwt_required()
def update_rsvp(event_id):
    """
    Update a user's RSVP status for an event.
    """
    data = request.get_json()
    rsvp_status = data.get('rsvp_status')  # Expected values: "attending", "not_attending", "maybe"

    # Validate RSVP status
    if rsvp_status not in ["attending", "not_attending", "maybe"]:
        return jsonify({"message": "Invalid RSVP status"}), 400

    # Validate event ID
    try:
        event_id = ObjectId(event_id)
    except Exception as e:
        return jsonify({"message": "Invalid event ID"}), 400

    # Get the current user's ID from the JWT token
    current_user_email = get_jwt_identity()
    user = users_collection.find_one({"email": current_user_email})
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_id = user['user_id']

    # Check if the event exists
    event = events_collection.find_one({"_id": event_id})
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Update the user's RSVP status
    events_collection.update_one(
        {"_id": event_id, "attendees": user_id},
        {"$set": {"rsvp_status": rsvp_status}}
    )

    return jsonify({"message": "RSVP status updated successfully"}), 200
