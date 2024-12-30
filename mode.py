from flask import Blueprint, request, render_template, redirect, url_for
from extensions import db
from models import AllDebate

mode_bp = Blueprint('mode', __name__, url_prefix='/mode')

@mode_bp.route('/mode_selection', methods=['GET'])
def mode_selection():
    modes = ['やさしい', 'ふつう', 'むずかしい']
    return render_template('mode.html', modes=modes)

@mode_bp.route('/save_mode', methods=['POST'])
def save_mode():
    mode = request.form.get('mode')
    debate = AllDebate.query.first()
    if debate:
        debate.mode = mode
        db.session.commit()
    return redirect(url_for('category.category_selection'))
