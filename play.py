# from flask import Flask, render_template, jsonify, request
# from character_creation import create_character
# from combat_system import win_or_loss, select_enemy
# from armor_weapon import weapon_options, armor_options

# app = Flask(__name__)

# character = None  # Global variable to store the character

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/create_character')
# def create_character_route():
#     global character
#     character = create_character()
#     return jsonify(character.__dict__)

# @app.route('/equip_weapon', methods=['POST'])
# def equip_weapon_route():
#     global character
#     if character:
#         weapon_index = request.json.get('weapon_index')
#         if 0 <= weapon_index < len(weapon_options):
#             character.equip_weapon(weapon_options[weapon_index])
#             return jsonify(character.__dict__)
#     return jsonify({'error': 'Character not created or invalid weapon index'}), 400

# @app.route('/equip_armor', methods=['POST'])
# def equip_armor_route():
#     global character
#     if character:
#         armor_index = request.json.get('armor_index')
#         if 0 <= armor_index < len(armor_options):
#             character.equip_armor(armor_options[armor_index])
#             return jsonify(character.__dict__)
#     return jsonify({'error': 'Character not created or invalid armor index'}), 400

# @app.route('/start_combat', methods=['POST'])
# def start_combat_route():
#     global character
#     if character:
#         enemy_name = request.json.get('enemy_name', 'Goblin')  # Default to Goblin if no enemy name is provided
#         enemy = select_enemy(enemy_name)
#         if enemy:
#             result = win_or_loss(character, enemy)
#             return jsonify({'result': result, 'character': character.__dict__})
#     return jsonify({'error': 'Character not created or enemy not found'}), 400

# if __name__ == '__main__':
#     app.run(debug=True)

from Menu import main_menu

def main():
    main_menu()

if __name__ == "__main__":
    main()