import sys
import os
from flask import Flask, jsonify, render_template, request
from game.models import db 
from game.views import game_bp  # Import the blueprint
from game.command_parser import parse_command, initialize_game_world
from game.combat import combat
from game.inventory import add_item, use_item
from game.game_state import GameState
from game.models import PlayerInventory 

def create_app():
    app = Flask(__name__)

    # Configure the Flask app to use the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(game_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/start')
    def start_game_route():
        GameState.location, GameState.inventory = initialize_game_world()
        GameState.update_location(GameState.location)  # Update the location
        return GameState.get_description()

    @app.route('/command', methods=['POST'])
    def command():
        data = request.get_json()
        user_input = data.get('input').lower()
        response = handle_command(user_input)
        return jsonify(response)

    @app.route('/combat', methods=['POST'])
    def handle_combat():
        player_inventory = PlayerInventory.query.first()  # A single player for now
        monster_id = request.json['monster_id']
        monster = monster.query.get(monster_id)  # assuming Monster is the model for monsters
        result = combat(player_inventory, monster)
        return jsonify(result)

    @app.route('/inventory/add', methods=['POST'])
    def handle_add_item():
        item_name = request.json['item_name']
        result = add_item(item_name)
        return jsonify(result)

    @app.route('/inventory/use', methods=['POST'])
    def handle_use_item():
        item_name = request.json['item_name']
        result = use_item(item_name)
        return jsonify(result)

    return app

def handle_command(command):
    GameState
    action, params = parse_command(command)

    if action == "go":
        if params:
            direction = ' '.join(params)
            new_location = determine_new_location(direction)
            if new_location:
                GameState.change_location(new_location)
                GameState.update_location(GameState.location)  # Update the location
                response = GameState.get_description()
            else:
                response = "You can't go that way."
        else:
            response = "Go where?"

    elif action == "inventory":
        response = GameState.list_items() 
    elif action == "use":
        if params:
            item_name = ' '.join(params)
            response = GameState.use_item(item_name)
        else:
            response = "Use what?"
    elif action == "quit":
        response = "Quitting the game..."
        # Add logic for quitting the game
    elif action == "help":
        response = "Available commands: go, inventory, use, quit, help."
    else:
        response = "Unknown command."

    return {
        'response': response,
        'state': {
            'location': GameState.location,
            'description': GameState.get_description(),
            'inventory': GameState.list_items()
        }
    }


def parse_command(command):
    parts = command.split()
    if not parts:
        return None, None
    action = parts[0]
    params = parts[1:]
    return action, params

def determine_new_location(direction):
    # Define the location mappings
    location_mappings = {
        'base_of_the_tower': {
            'north': 'forest_entrance',
            'south': 'return_to_village',
            'east': 'guardhouse_entrance',
            'west': 'marsh_entrance',
            'to tower entrance': 'tower_entrance',
            'to tower': 'tower_entrance',
            'to the tower entrance': 'tower_entrance',
            'to the tower': 'tower_entrance'
        },
        'forest_entrance': {
            'south': 'base_of_the_tower',
            'further into the forest': 'forest_clearing',
            'further': 'forest_clearing'
        },
        'forest_clearing': {
            'back': 'forest_entrance',
            'forest entrance': 'forest_entrance',
            'entrance': 'forest_entrance',
            'west': 'forest_west',
            'east': 'forest_east',
            'north': 'forest_north'
        },
        'forest_west': {
            'back': 'forest_clearing',
            'forest clearing': 'forest_clearing',
            'to skeleton': 'forest_rucksack',
            'to rucksack': 'forest_rucksack',
            'to adventurer': 'forest_rucksack',
            'further': 'forest_west_warning'
        },
        'forest_rucksack': {
            'forest clearing': 'forest_clearing',
            'further': 'forest_west_warning',
            'west': 'forest_west_warning'
        },
        'forest_west_warning': {
            'forest clearing': 'forest_clearing',
            'back': 'forest_west',
            'further': 'forest_west_death'
        },
        'forest_west_death': {
            'restart': 'forest_entrance'
        },
        'forest_east': {
            'back': 'forest_clearing',
            'west': 'forest_clearing',
            'to cave': 'cave_entrance',
            'to the cave': 'cave_entrance'
        },
        'cave_entrance': {
            'out': 'forest_east',
            'back': 'forest_east',
            'enter': 'cave_interior',
            'inside': 'cave_interior'
        },
        'cave_interior': {
            'out': 'cave_entrance',
            'back': 'cave_entrance',
            'further': 'cave_light',
            'to light': 'cave_light'
        },
        'cave_light': {
            'west': 'cave_interior',
            'up': 'dungeon_cave_entrance'
        },
        'dungeon_cave_entrance': {
            'back': 'cave_entrance',
            'into dungeon': 'tower_dungeon',
            'inside': 'tower_dungeon'
        },
        'tower_dungeon': {
            'first floor': 'tower_first_floor',
            'to apprentice': 'tower_dungeon_apprentice',
            'to cell': 'tower_dungeon_apprentice'
        },
        'tower_dungeon_apprentice': {
            'to first floor': 'tower_first_floor',
            'to secret entrance': 'second_floor_secret_entrance',
            'to second floor': 'second_floor_secret_entrance'
        },
        "second_floor_secret_entrance": {
            'to second floor': 'tower_second_floor',
            'to first floor': 'tower_first_floor'
        },
        'return_to_village': {
            'north': 'base_of_the_tower',
            'to village': 'village_ending',
            'to the village': 'village_ending'
        },
        'guardhouse_entrance': {
            'west': 'base_of_the_tower',
            'upstairs': 'guardhouse_upstairs',
            'to table': 'guardhouse_table',
            'to weapons rack': 'guardhouse_weapons_rack'
        },
        'guardhouse_table': {
            'to entrance': 'guardhouse_entrance',
            'back': 'guardhouse_entrance'
        },
        'guardhouse_weapons_rack': {
            'to entrance': 'guardhouse_entrance',
            'back': 'guardhouse_entrance'
        },
        'guardhouse_upstairs': {
            'downstairs': 'guardhouse_entrance',
            'to chest': 'guardhouse_chest'
        },
        'guardhouse_chest': {
            'downstairs': 'guardhouse_entrance',
            'back': 'guardhouse_upstairs'
        },
        'marsh_entrance': {
            'east': 'base_of_the_tower',
            'further': 'marsh_depths'
        },
        'marsh_depths': {
            'back': 'marsh_entrance',
            'marsh entrance': 'marsh_entrance',
            'to chest': 'marsh_chest',
            'further': 'marsh_secret'
        },
        'marsh_chest': {
            'back': 'marsh_depths',
            'marsh depths': 'marsh_depths',
            'further': 'marsh_secret'
        },
        'marsh_secret': {
            'back': 'marsh_depths',
            'marsh depths': 'marsh_depths'
        },
        'tower_entrance': {
            'scion': 'tower_foyer',
            'back': 'base_of_the_tower'
        },
        'tower_foyer': {
            'up': 'tower_first_floor',
            'to first floor': 'tower_first_floor',
            'to dungeon': 'tower_dungeon',
            'down': 'tower_dungeon'
        },
        'tower_first_floor': {
            'down': 'tower_foyer',
            'to foyer': 'tower_foyer',
            'north': 'first_floor_north_room',
            'east': 'first_floor_east_room',
            'west': 'first_floor_west_room',
            'to stairs': 'tower_dungeon'
        },
        'first_floor_north_room': {
            'south': 'tower_first_floor',
            'to first floor': 'tower_first_floor'
        },
        'first_floor_east_room': {
            'west': 'tower_first_floor',
            'to first floor': 'tower_first_floor'
        },
        'first_floor_west_room': {
            'east': 'tower_first_floor',
            'to first floor': 'tower_first_floor'
        },
        'tower_second_floor': {
            'down': 'tower_first_floor',
            'to first floor': 'tower_first_floor',
            'north': 'second_floor_north_room',
            'east': 'second_floor_east_room',
            'west': 'second_floor_west_room'
        },
        'second_floor_north_room': {
            'south': 'tower_second_floor',
            'to second floor': 'tower_second_floor'
        },
        'second_floor_east_room': {
            'west': 'tower_second_floor',
            'to second floor': 'tower_second_floor'
        },
        'second_floor_west_room': {
            'east': 'tower_second_floor',
            'to second floor': 'tower_second_floor',
            'to apprentice': 'second_floor_apprentice'
        },
        'second_floor_apprentice': {
            'fight': 'apprentice_battle'
        },
        'apprentice_battle': {
            'back': 'second_floor_west_room',
            'to third floor': 'tower_third_floor',
            'to the third floor': 'tower_third_floor',
            'up': 'tower_third_floor'
        },
        'tower_third_floor': {
            'down': 'tower_second_floor',
            'to second floor': 'tower_second_floor',
            'north': 'third_floor_north_room',
            'east': 'third_floor_east_room',
            'west': 'third_floor_west_room',
            'to apprentice': 'third_floor_apprentice'
        },
        'third_floor_north_room': {
            'south': 'tower_third_floor',
            'to third floor': 'tower_third_floor',
            'break barrier': 'break_barrier_event',
            'break the barrier': 'break_barrier_event'
        },
        'third_floor_east_room': {
            'west': 'tower_third_floor',
            'to third floor': 'tower_third_floor'
        },
        'third_floor_west_room': {
            'east': 'tower_third_floor',
            'to third floor': 'tower_third_floor'
        },
        'third_floor_apprentice': {
            'back': 'tower_third_floor',
        },
        'break_barrier_event': {
            'fight': 'apprentice_third_battle'
        },
        'apprentice_third_battle': {
            'to third floor': 'tower_third_floor',
            'back': 'tower_third_floor',
            'to fourth floor': 'tower_fourth_floor'
        },
        'tower_fourth_floor': {
            'down': 'tower_third_floor',
            'to third floor': 'tower_third_floor',
            'north': 'fourth_floor_north_room',
            'east': 'fourth_floor_east_room',
            'west': 'fourth_floor_west_room'
        },
        'fourth_floor_north_room': {
            'south': 'tower_fourth_floor',
            'to fourth floor': 'tower_fourth_floor'
        },
        'fourth_floor_east_room': {
            'west': 'tower_fourth_floor',
            'to fourth floor': 'tower_fourth_floor'
        },
        'fourth_floor_west_room': {
            'east': 'tower_fourth_floor',
            'to fourth floor': 'tower_fourth_floor',
            'to the apprentice': 'fourth _floor_apprentice'
        },
        'fourth_floor_apprentice': {
            'fight': 'apprentice_fourth_battle'
        },
        'apprentice_fourth_battle': {
            'to fourth floor': 'tower_fourth_floor',
            'back': 'tower_fourth_floor',
            'to fifth floor': 'tower_fifth_floor',
            'to the fifth floor': 'tower_fifth_floor'
        },
        'tower_fifth_floor': {
            'down': 'tower_fourth_floor',
            'to fourth floor': 'tower_fourth_floor',
            'north': 'fifth_floor_north_room',
            'east': 'fifth_floor_east_room',
            'west': 'fifth_floor_west_room'
        },
        'fifth_floor_north_room': {
            'south': 'tower_fifth_floor',
            'to fifth floor': 'tower_fifth_floor'
        },
        'fifth_floor_east_room': {
            'west': 'tower_fifth_floor',
            'to fifth floor': 'tower_fifth_floor',
            'to Valthor': 'fifth_floor_valthor'
        },
        'fifth_floor_west_room': {
            'east': 'tower_fifth_floor',
            'to fifth floor': 'tower_fifth_floor'
        },
        'fifth_floor_valthor': {
            'fight': 'valthor_battle'
        },
        'valthor_battle': {
            'to fifth floor': 'tower_fifth_floor',
            'to victory': 'victory_scene'
        },
        'victory_scene': {
            'to start': 'base_of_the_tower',
            'restart': 'base_of_the_tower'
        }      
    }

    current_location = GameState.location
    if current_location in location_mappings and direction in location_mappings[current_location]:
        return location_mappings[current_location][direction]
    else:
        return None

def explore_location(location):
     GameState.previous_location

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

