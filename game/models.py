from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()

engine = create_engine('sqlite:///game.db')

class item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    damage = db.Column(db.Integer, nullable=True)
    heal = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(200), nullable=True)  # Added description field

class monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    damage = db.Column(db.Integer, nullable=False)

class PlayerInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health = db.Column(db.Integer, nullable=False)
    max_health = db.Column(db.Integer, nullable=False)
    items = db.relationship('item', secondary='inventory_items')

inventory_items = db.Table('inventory_items',
    db.Column('player_inventory_id', db.Integer, db.ForeignKey('player_inventory.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)
