from .models import db, PlayerInventory, item

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def has_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None

class item:
    def __init__(self, name, damage=0, heal=0):
        self.name = name
        self.damage = damage
        self.heal = heal

def add_item(item_name):
    player_inventory = PlayerInventory.query.first()
    if len(player_inventory.items) < 8:
        item = item.query.filter_by(name=item_name).first()
        player_inventory.items.append(item)
        db.session.commit()
        return {"message": "Item added", "item": item_name}
    return {"message": "Inventory full"}

def remove_item(item_name):
    player_inventory = PlayerInventory.query.first()
    item = item.query.filter_by(name=item_name).first()
    
    if item in player_inventory.items:
        player_inventory.items.remove(item)
        db.session.commit()
        return {"message": "Item removed", "item": item_name}
    
    return {"message": "Item not found"}

def use_item(item_name):
    player_inventory = PlayerInventory.query.first()
    item = item.query.filter_by(name=item_name).first()
    if item_name == 'greater health potion' or 'health potion' and item in player_inventory.items:
        player_inventory.health = min(player_inventory.max_health, player_inventory.health + item.heal)
        player_inventory.items.remove(item)
        db.session.commit()
        return {"message": "Used potion", "health": player_inventory.health}
    return {"message": "Cannot use item"}
