# game/views.py

from .game_state import GameState

def setup_views(game_bp, app):
    @game_bp.route('/')
    def index():
        # Use GameState here with the app instance
        game_state = GameState(app)
        # ...
