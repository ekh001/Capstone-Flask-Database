from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Destination, DestinationSchema, destination_schema, destinations_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'apples': 'bananas'}


# Insert destination into database

@api.route('/itinerary', methods = ['POST'])
@token_required
def create_destination_data(current_user_token):
    name = request.json['name']
    location = request.json['location']
    category = request.json['category']
    notes = request.json['notes']
    user_token = current_user_token.token

    print(f'BIG TEST: {current_user_token.token}')

    destination = Destination(name, location, category, notes, user_token = user_token )

    db.session.add(destination)
    db.session.commit()

    response = destination_schema.dump(destination)
    return jsonify(response)

# Retrieve all destinations

@api.route('/itinerary', methods = ['GET'])
@token_required
def get_destination(current_user_token):
    a_user = current_user_token.token
    destinations = Destination.query.all()
    response = destinations_schema.dump(destinations)
    return jsonify(response)

# Retrieve a single destination

@api.route('/itinerary/<id>', methods = ['GET'])
@token_required
def get_single_destination(current_user_token, id):
    destination = Destination.query.get(id)
    response = destination_schema.dump(destination)
    return jsonify(response)

# Update destination info

@api.route('/itinerary/<id>', methods = ['POST','PUT'])
@token_required
def update_destination(current_user_token,id):
    destination = Destination.query.get(id) 
    destination.name = request.json['name']
    destination.location = request.json['location']
    destination.category = request.json['category']
    destination.notes = request.json['notes']
    destination.user_token = current_user_token.token

    db.session.commit()
    response = destination_schema.dump(destination)
    return jsonify(response)

# Delete a destination

@api.route('/itinerary/<id>', methods = ['DELETE'])
@token_required
def delete_destination(current_user_token, id):
    destination = Destination.query.get(id)
    db.session.delete(destination)
    db.session.commit()
    response = destination_schema.dump(destination)
    return jsonify(response)   