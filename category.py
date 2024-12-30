from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db

category_bp = Blueprint('category', __name__)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

@category_bp.route('/category_page')
def category_selection():
    categories = ['環境問題', '教育', '社会問題', "就活"]
    return render_template('category.html', categories=categories)

@category_bp.route('/debate_page', methods=['POST'])
def submit_topic():
    category = request.form.get("category")
    free_text = request.form.get("free_text")

    if category:
        new_category = Category(category=category)
        db.session.add(new_category)
    if free_text:
        new_topic = Topic(text=free_text)
        db.session.add(new_topic)

    db.session.commit()
    return redirect(url_for('debate.debate'))
