# game/routes.py

from flask import Blueprint, render_template
from .views import setup_views

game_bp = Blueprint('game', __name__, template_folder='templates')
setup_views(game_bp) 
