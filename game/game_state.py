from game.inventory import Player
from db_setup import get_item_from_db, get_monster_from_db  # Import functions from db_setup.py

# Function to initialize starter inventory
def initialize_starter_inventory():
    # Assuming item_id 1 is for dagger and item_id 2 is for health potion
    starter_inventory = [
        get_item_from_db(3),  # Dagger
        get_item_from_db(10),  # Health Potion
    ]
    return starter_inventory

class GameState:
    location = None  # Define the location attribute at the class level

    def __init__(self):
        self.player = Player('Hero')
        self.previous_location = None
        self.location = 'base_of_the_tower'

        # Define the locations with items and monsters
        self.location_items = {
            'forest_rucksack': [get_item_from_db(10)],  # health potion
            'guardhouse_chest': [get_item_from_db(1)], # short sword
            'tower_dungeon_apprentice': [get_item_from_db(8)], # staff
            'first_floor_east_room': [get_item_from_db(10)], # health potion
            'second_floor_north_room': [get_item_from_db(2)], # long sword
            'third_floor_west_room': [get_item_from_db(11)], # greater health potion 
            'forth_floor_east_room': [get_item_from_db(9)], # warhammer
            'fifth_floor_north_room': [get_item_from_db(11)], # greater health potion
            'fifth_floor_west_room': [get_item_from_db(8)] # greatsword
        }

        self.location_monsters = {
            'tower_dungeon': get_monster_from_db(1),  # skeleton
            'first_floor_west_room': get_monster_from_db(2), # goblin
            'first_floor_north_room': get_monster_from_db(7), # zombie
            'second_floor_east_room': get_monster_from_db(6), # flesh golem
            'third_floor_east_room': get_monster_from_db(3), # spectral knight
            'fourth_floor_north_room': get_monster_from_db(4), # troll
            'tower_fifth_floor': get_monster_from_db(5), # wraith
            'second_floor_apprentice': get_monster_from_db(8), # apprentice 1 
            'third_floor_apprentice': get_monster_from_db(9), # apprentice 2
            'fourth_floor_apprentice': get_monster_from_db(10), # apprentice 3
            'fifth_floor_valthor': get_monster_from_db(11) # Valthor
        }

    def get_description(self):
        description = f"You are at {self.location}.\n"
        
        # Check if there are items in the current location
        if self.location_items.get(self.location):
            description += "You see the following items:\n"
            for item in self.location_items[self.location]:
                description += f"- {item.name}\n"
        
        # Check if there are monsters in the current location
        if self.location_monsters.get(self.location):
            description += "You are facing the following monsters:\n"
            for monster in self.location_monsters[self.location]:
                description += f"- {monster.name} (Health: {monster.health}, Damage: {monster.damage})\n"
        
        return description.strip()
    
    def list_items(self):
        inventory_list = "Inventory:\n"
        for item in self.player.inventory:
            inventory_list += f"- {item.name}\n"
        return inventory_list.strip()
       
# Create an instance of GameState
game_state = GameState()

# Call the get_description method on the instance
description = game_state.get_description()  
