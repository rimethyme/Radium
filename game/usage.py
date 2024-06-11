from models import db, item

def use_quest_item(item_name):
    # Query the item from the database
    item = item.query.filter_by(name=item_name).first()

    # Check if the item exists and is a quest item
    if item and item.is_quest_item:
        # Check if the item is already used
        if not item.is_used:
            # Update the item's status to indicate it's been used
            item.is_used = True
            db.session.commit()
            return {"message": f"{item_name} has been used."}
        else:
            return {"message": f"{item_name} is already used."}
    else:
        return {"message": f"{item_name} is not a quest item or does not exist."}

def use_stackable_item(item_name):
    # Query the item from the database
    item = item.query.filter_by(name=item_name).first()

    # Check if the item exists and is stackable
    if item and item.is_stackable:
        # Implement logic for using stackable items
        return {"message": f"{item_name} has been used."}
    else:
        return {"message": f"{item_name} is not a stackable item or does not exist."}

# Add more functions for other types of item usage as needed
