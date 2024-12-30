from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db

mode_bp = Blueprint('mode', __name__)

class Mode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.String(20), nullable=False)

@mode_bp.route('/')
def mode_selection():
    modes = ['やさしい', 'ふつう', 'むずかしい']
    return render_template('mode.html', modes=modes)

@mode_bp.route('/category_page', methods=['POST'])
def next_category_page():
    mode = request.form["mode"]
    new_mode = Mode(mode=mode)
    db.session.add(new_mode)
    db.session.commit()
    return redirect(url_for('category.category_selection'))
