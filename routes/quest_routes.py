from flask import Blueprint

import controllers

quest = Blueprint("quest", __name__)

@quest.route('/quest', methods=['POST'])
def add_quest_route():
    return controllers.add_quest()

@quest.route('/quests', methods=['GET'])
def get_all_quests_route():
    return controllers.get_all_quests()

@quest.route('/quest/<quest_id>', methods=['GET'])
def get_quest_by_id_route(quest_id):
    return controllers.get_quest_by_id(quest_id)

@quest.route('/quest/difficulty/<difficulty_level>', methods=['GET'])
def get_quest_by_difficulty_level_route(difficulty_level):
    return controllers.get_quests_by_difficulty_level(difficulty_level)

@quest.route('/quest/<quest_id>', methods=['PUT'])
def update_quest_by_id_route(quest_id):
    return controllers.update_quest_by_id(quest_id)

@quest.route('/quest/<quest_id>/complete', methods=['PATCH'])
def complete_quest_by_id_route(quest_id):
    return controllers.complete_quest_by_id(quest_id)

@quest.route('/quest/delete/<quest_id>', methods=['DELETE'])
def delete_quest_by_id_route(quest_id):
    return controllers.delete_quest_by_id(quest_id)
