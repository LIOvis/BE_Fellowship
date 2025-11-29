from flask import Blueprint

import controllers

ability = Blueprint("ability", __name__)

@ability.route('/ability', methods=['POST'])
def add_ability_route():
    return controllers.add_ability()

@ability.route('/abilities', methods=['GET'])
def get_all_abilities_route():
    return controllers.get_all_abilities()

@ability.route('/ability/<ability_id>', methods=['GET'])
def get_ability_by_id_route(ability_id):
    return controllers.get_ability_by_id(ability_id)

@ability.route('/ability/<ability_id>', methods=['PUT'])
def update_ability_by_id_route(ability_id):
    return controllers.update_ability_by_id(ability_id)

@ability.route('/ability/delete/<ability_id>', methods=['DELETE'])
def delete_ability_by_id_route(ability_id):
    return controllers.delete_ability_by_id(ability_id)
