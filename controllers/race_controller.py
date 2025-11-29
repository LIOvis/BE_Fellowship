from flask import request, jsonify

from models.race import Races, races_schema, race_schema
from util.reflection import populate_object
from db import db

def add_race():
    post_data = request.form if request.form else request.json

    new_race = Races.new_race_obj()

    populate_object(new_race, post_data)

    try:
        db.session.add(new_race)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add race"}), 400
    
    return jsonify({"message": "race added", "result": race_schema.dump(new_race)}), 201

def get_all_races():
    query = db.session.query(Races).all()

    return jsonify({"message": "races found", "results": races_schema.dump(query)}), 200

def get_race_by_id(race_id):
    query = db.session.query(Races).filter(Races.race_id == race_id).first()

    if not query:
        return jsonify({"message": "race not found"}), 404
    
    return jsonify({"message": "race found", "result": race_schema.dump(query)}), 200

def update_race_by_id(race_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Races).filter(Races.race_id == race_id).first()

    if not query:
        return jsonify({"message": "race not found"}), 404
    
    try:
        populate_object(query, post_data)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update race"}), 400
    
    return jsonify({"message": "race updated", "result": race_schema.dump(query)}), 200

def delete_race_by_id(race_id):
    query = db.session.query(Races).filter(Races.race_id == race_id).first()

    if not query:
        return jsonify({"message": "race not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete race"}), 400
    
    return jsonify({"message": "race deleted"}), 200