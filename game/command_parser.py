import random
from game.models import PlayerInventory

def parse_input(user_input):
    # Normalize input to lowercase
    user_input = user_input.lower()
    
    # Define the valid commands
    valid_commands = ['go', 'inventory', 'look', 'search', 'attack', 'use', 'quit']
    
    # Check if the user input matches any valid command
    if user_input in valid_commands:
        return user_input
    else:
        return None  # Invalid command

def parse_command(command):
    # Split the command into action and parameters
    parts = command.split()
    if not parts:
        return None, []
    action = parts[0]
    params = parts[1:]
    return action, params

# Function to initialize the game world
def initialize_game_world():
    # Set up the player's starting location
    player_location = "base of the tower"
    
    # Initialize player inventory
    player_inventory = PlayerInventory(health=100, max_health=100, items=[])
    
    return player_location, player_inventory

# Function to handle combat between the player and a monster
def initiate_combat(player_inventory, monster):
    player_health = player_inventory.health
    monster_health = monster.health
    
    print(f"A wild {monster.name} appears!")

    while player_health > 0 and monster_health > 0:
        print("Player Health:", player_health)
        print("Monster Health:", monster_health)
        print("Options:")
        print("1. Attack")
        print("2. Run")
        choice = input("Choose your action: ")

        # Normalize user input to lowercase
        choice = choice.lower()

        if choice == "1" or choice == "attack":
            if not player_inventory.items:
                print("You don't have any weapons to attack with!")
                continue  # Continue the loop to prompt the user again
            player_damage = player_inventory.items[0].damage  # Assuming the first item is a weapon
            monster_health -= player_damage
            print("You attacked the", monster.name + "!")
            if monster_health <= 0:
                print("You defeated the", monster.name + "!")
                return "win"
        elif choice == "2" or choice == "run":
            if random.random() < 0.5:
                print("You managed to escape!")
                return "flee"
            else:
                print("You couldn't escape!")
                player_health -= monster.damage
                if player_health <= 0:
                    print("You were defeated by the", monster.name + "!")
                    return "lose"
        else:
            print("Invalid choice. Try again.")

    return "draw"  # This should only happen if both the player and monster have 0 health at the same time
