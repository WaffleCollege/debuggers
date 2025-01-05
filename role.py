from flask import Blueprint, request, redirect, url_for, render_template
from extensions import db
from models import AllDebate


role_bp = Blueprint('role', __name__)

@role_bp.route('/set_role', methods=['POST'])
def set_role():
    position = request.form.get('position')

    # ユーザーの選択に基づいてデータを設定
    if position == '先攻':
        user_1 = "ユーザー"
        user_2 = "AI"
    elif position == '後攻':
        user_1 = "AI"
        user_2 = "ユーザー"
    else:
        return "Invalid position", 400

    # `AllDebate`テーブルに保存
    new_debate = AllDebate(
        user_1=user_1,
        user_2=user_2,
        mode=None,  # 初期値としてNoneを設定
        category=None,
        topic=None
    )
    db.session.add(new_debate)
    db.session.commit()

    # debate画面にリダイレクト
    return redirect(url_for('debate.start_debate'))


@role_bp.route('/role_selection', methods=['GET'])
def role_selection():
    debate = AllDebate.query.first()
    if not debate or (not debate.category and not debate.topic):
        return redirect(url_for('category.category_selection'))  # カテゴリー未選択時に戻す

    return render_template(
        'role.html',
        category=debate.category,
        topic=debate.topic
    )
