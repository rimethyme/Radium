from flask import Blueprint, render_template

game_bp = Blueprint('game', __name__, template_folder='templates')

@game_bp.route('/')
def index():
    return render_template('index.html')
