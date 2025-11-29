from flask import request, jsonify

from models.ability import Abilities, abilities_schema, ability_schema
from util.reflection import populate_object
from db import db

def add_ability():
    post_data = request.form if request.form else request.json

    new_ability = Abilities.new_ability_obj()

    populate_object(new_ability, post_data)

    try:
        db.session.add(new_ability)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add ability"}), 400
    
    return jsonify({"message": "ability added", "result": ability_schema.dump(new_ability)}), 201

def get_all_abilities():
    query = db.session.query(Abilities).all()

    return jsonify({"message": "abilities found", "results": abilities_schema.dump(query)}), 200

def get_ability_by_id(ability_id):
    query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if not query:
        return jsonify({"message": "ability not found"}), 404
    
    return jsonify({"message": "ability found", "result": ability_schema.dump(query)}), 200

def update_ability_by_id(ability_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if not query:
        return jsonify({"message": "ability not found"}), 404
    
    try:
        populate_object(query, post_data)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update ability"}), 400
    
    return jsonify({"message": "ability updated", "result": ability_schema.dump(query)}), 200

def delete_ability_by_id(ability_id):
    query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if not query:
        return jsonify({"message": "ability not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete ability"}), 400
    
    return jsonify({"message": "ability deleted"}), 200