from flask import request, jsonify

from models.quest import Quests, quests_schema, quest_schema
from util.reflection import populate_object
from db import db

def add_quest():
    post_data = request.form if request.form else request.json

    new_quest = Quests.new_quest_obj()

    populate_object(new_quest, post_data)

    try:
        db.session.add(new_quest)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add quest"}), 400
    
    return jsonify({"message": "quest added", "result": quest_schema.dump(new_quest)}), 201

def get_all_quests():
    query = db.session.query(Quests).all()

    return jsonify({"message": "quests found", "results": quests_schema.dump(query)}), 200

def get_quest_by_id(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not query:
        return jsonify({"message": "quest not found"}), 404
    
    return jsonify({"message": "quest found", "result": quest_schema.dump(query)}), 200

def get_quests_by_difficulty_level(difficulty_level):
    query = db.session.query(Quests).filter(Quests.difficulty == difficulty_level).all()

    return jsonify({"message": "quests found", "results": quests_schema.dump(query)}), 200

def update_quest_by_id(quest_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not query:
        return jsonify({"message": "quest not found"}), 404
    
    try:
        populate_object(query, post_data)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update quest"}), 400
    
    return jsonify({"message": "quest updated", "result": quest_schema.dump(query)}), 200

def complete_quest_by_id(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not query:
        return jsonify({"message": "quest not found"}), 404
    
    try:
        populate_object(query, {"is_completed": True})
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to complete quest"}), 400
    
    return jsonify({"message": "quest completed", "result": quest_schema.dump(query)}), 200

def delete_quest_by_id(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not query:
        return jsonify({"message": "quest not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete quest"}), 400
    
    return jsonify({"message": "quest deleted"}), 200