import sqlite3
from game.models import db, item, monster  # Import models directly

def connect_db():
    return sqlite3.connect('game.db')

def get_monster(monster_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, health, damage FROM monster WHERE id=?", (monster_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {'name': result[0], 'health': result[1], 'damage': result[2]}
    return None

def get_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, damage, heal FROM item WHERE id=?", (item_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {'name': result[0], 'damage': result[1], 'heal': result[2]}
    return None

def get_item_from_db(item_id):
    item_data = get_item(item_id)
    if item_data:
        return item(name=item_data['name'], damage=item_data['damage'], heal=item_data['heal'])
    return None

def get_monster_from_db(monster_id):
    monster_data = get_monster(monster_id)
    if monster_data:
        return monster(name=monster_data['name'], health=monster_data['health'], damage=monster_data['damage'])
    return None

# Initialize database within Flask application context
def init_db(app):
    with app.app_context():
        db.create_all()

        # Add initial items
        
        # Weapons
        short_sword = item(name='short sword', description='A lightweight sword ideal for close combat.', damage=6)
        long_sword = item(name='long sword', description='A powerful sword with a long blade.', damage=10)
        starter_dagger = item(name='rusty dagger', description='A small, sharp blade designed for quick strikes.', damage=5)
        battle_axe = item(name='battle axe', description='A heavy axe with a broad blade, perfect for cleaving through enemies.', damage=12)
        spear = item(name='spear', description='A long, pointed weapon with a wooden shaft, effective for thrusting attacks.', damage=9)
        two_handed_sword = item(name='two-handed sword', description='A massive sword requiring two hands to wield, delivering devastating blows.', damage=15)
        staff = item(name='staff', description='A wooden staff wielded by mages.', damage=8)
        greatsword = item(name='greatsword', description='A massive sword known for its sheer size and cutting power.', damage=15)
        warhammer = item(name='warhammer', description='A massive hammer designed for crushing blows.', damage=13)

        # Misc items
        health_potion = item(name='health potion', description='A potion that restores a little health.', heal=15)
        greater_health_potion = item(name='greater health potion', description='A potion that restores some health.', heal=25)

        db.session.add(short_sword)
        db.session.add(long_sword)
        db.session.add(starter_dagger)
        db.session.add(battle_axe)
        db.session.add(spear)
        db.session.add(two_handed_sword)
        db.session.add(staff)
        db.session.add(greatsword)
        db.session.add(warhammer)
        db.session.add(health_potion)
        db.session.add(greater_health_potion)

        # Monsters
        skeleton = monster(name='skeleton', health=25, damage=5)
        goblin = monster(name='goblin', health=15, damage=4)
        spectral_knight = monster(name='spectral knight', health=35, damage=8)
        troll = monster(name='troll', health=40, damage=10)
        wraith = monster(name='wraith', health=45, damage=7)
        flesh_golem = monster(name='flesh golem', health=30, damage=7)
        zombie = monster(name= 'zombie', health=20, damage=5)
        apprentice_1 = monster(name= 'edwin the lesser', health=40, damage=8)
        apprentice_2 = monster(name= 'the hooded one', health=50, damage=10)
        apprentice_3 = monster(name= 'sorin sagewort', health=60, damage=12)
        valthor = monster(name= 'valthor', health= 70, damage=15)

        # Add monsters to the database session
        db.session.add(skeleton)
        db.session.add(goblin)
        db.session.add(spectral_knight)
        db.session.add(troll)
        db.session.add(wraith)
        db.session.add(flesh_golem)
        db.session.add(zombie)
        db.session.add(apprentice_1)
        db.session.add(apprentice_2)
        db.session.add(apprentice_3)
        db.session.add(valthor)

        # Commit changes to the database
        db.session.commit()
