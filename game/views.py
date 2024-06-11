# game/views.py

from .game_state import GameState

def setup_views(game_bp):
    @game_bp.route('/')
    def index():
        # Use GameState here
        game_state = GameState()
        # ...
