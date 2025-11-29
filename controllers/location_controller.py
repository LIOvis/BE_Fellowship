from flask import request, jsonify

from models.location import Locations, locations_schema, location_schema
from util.reflection import populate_object
from db import db

def add_location():
    post_data = request.form if request.form else request.json

    new_location = Locations.new_location_obj()

    populate_object(new_location, post_data)

    try:
        db.session.add(new_location)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add location"}), 400
    
    return jsonify({"message": "location added", "result": location_schema.dump(new_location)}), 201

def get_all_locations():
    query = db.session.query(Locations).all()

    return jsonify({"message": "locations found", "results": locations_schema.dump(query)}), 200

def get_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()

    if not query:
        return jsonify({"message": "location not found"}), 404
    
    return jsonify({"message": "location found", "result": location_schema.dump(query)}), 200

def update_location_by_id(location_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()

    if not query:
        return jsonify({"message": "location not found"}), 404
    
    try:
        populate_object(query, post_data)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update location"}), 400
    
    return jsonify({"message": "location updated", "result": location_schema.dump(query)}), 200

def delete_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()

    if not query:
        return jsonify({"message": "location not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete location"}), 400
    
    return jsonify({"message": "location deleted"}), 200