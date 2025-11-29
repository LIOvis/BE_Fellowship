from flask import request, jsonify

from models.realm import Realms, realms_schema, realm_schema
from util.reflection import populate_object
from db import db

def add_realm():
    post_data = request.form if request.form else request.json

    new_realm = Realms.new_realm_obj()

    populate_object(new_realm, post_data)

    try:
        db.session.add(new_realm)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add realm"}), 400
    
    return jsonify({"message": "realm added", "result": realm_schema.dump(new_realm)}), 201

def get_all_realms():
    query = db.session.query(Realms).all()

    return jsonify({"message": "realms found", "results": realms_schema.dump(query)}), 200

def get_realm_by_id(realm_id):
    query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not query:
        return jsonify({"message": "realm not found"}), 404
    
    return jsonify({"message": "realm found", "result": realm_schema.dump(query)}), 200

def update_realm_by_id(realm_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not query:
        return jsonify({"message": "realm not found"}), 404
    
    try:
        populate_object(query, post_data)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update realm"}), 400
    
    return jsonify({"message": "realm updated", "result": realm_schema.dump(query)}), 200

def delete_realm_by_id(realm_id):
    query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not query:
        return jsonify({"message": "realm not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete realm"}), 400
    
    return jsonify({"message": "realm deleted"}), 200