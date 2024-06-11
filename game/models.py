from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class monster(db.Model):
    __tablename__ = 'monster'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    health = db.Column(db.Integer)
    damage = db.Column(db.Integer)

class item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    damage = db.Column(db.Integer)
    heal = db.Column(db.Integer)

class PlayerInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health = db.Column(db.Integer, nullable=False)
    max_health = db.Column(db.Integer, nullable=False)
    items = db.relationship('item', secondary='inventory_items')

inventory_items = db.Table('inventory_items',
    db.Column('player_inventory_id', db.Integer, db.ForeignKey('player_inventory.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)
