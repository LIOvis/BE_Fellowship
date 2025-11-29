from flask import request, jsonify

from models.hero import Heroes, heroes_schema, hero_schema
from models.hero_quest_xref import HeroesQuests, hero_quest_schema
from util.reflection import populate_object
from db import db

def add_hero():
    post_data = request.form if request.form else request.json

    new_hero = Heroes.new_hero_obj()

    populate_object(new_hero, post_data)

    try:
        db.session.add(new_hero)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add hero"}), 400
    
    return jsonify({"message": "hero added", "result": hero_schema.dump(new_hero)}), 201

def add_hero_quest():
    post_data = request.form if request.form else request.json

    new_hero_quest = HeroesQuests.new_hero_quest_obj()

    populate_object(new_hero_quest, post_data)

    try:
        db.session.add(new_hero_quest)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add hero-quest association"}), 400
    
    return jsonify({"message": "hero-quest association added", "result": hero_quest_schema.dump(new_hero_quest)}), 201

def get_all_heroes():
    query = db.session.query(Heroes).all()

    return jsonify({"message": "heroes found", "results": heroes_schema.dump(query)}), 200

def get_hero_by_id(hero_id):
    query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

    if not query:
        return jsonify({"message": "hero not found"}), 404
    
    return jsonify({"message": "hero found", "result": hero_schema.dump(query)}), 200

def get_all_alive_heroes():
    query = db.session.query(Heroes).filter(Heroes.is_alive == True).all()

    return jsonify({"message": "heroes found", "results": heroes_schema.dump(query)}), 200

def update_hero_by_id(hero_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

    if not query:
        return jsonify({"message": "hero not found"}), 404
    
    try:
        populate_object(query, post_data)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update hero"}), 400
    
    return jsonify({"message": "hero updated", "result": hero_schema.dump(query)}), 200

def delete_hero_by_id(hero_id):
    query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

    if not query:
        return jsonify({"message": "hero not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete hero"}), 400
    
    return jsonify({"message": "hero deleted"}), 200