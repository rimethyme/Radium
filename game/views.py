# game/views.py

from game.routes import game_bp
from .game_state import GameState

@game_bp.route('/')
def index():
    # Use GameState here
    game_state = GameState()
    # ...
 