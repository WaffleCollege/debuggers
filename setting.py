from flask import Blueprint, request, render_template, redirect, url_for
from extensions import db
from models import AllDebate

# モード選択、カテゴリー選択、ロール選択を一つのBlueprintに
setting_bp = Blueprint('setting', __name__)

@setting_bp.route('/setting', methods=['GET', 'POST'])
def setting():
    modes = ['やさしい', 'ふつう', 'むずかしい']
    categories = ['環境問題', '教育', '社会問題', 'テクノロジー']

    if request.method == 'POST':
        # フォームデータから値を取得
        mode = request.form.get('mode')
        category = request.form.get('category')
        topic = request.form.get('topic')
        position = request.form.get('position')
        start_button = request.form.get('start_button')

        # `AllDebate`レコードを取得または作成
        debate = AllDebate.query.first()
        if not debate:
            debate = AllDebate()  # レコードが存在しない場合は新規作成

        # データの更新
        debate.mode = mode
        debate.category = category
        debate.topic = topic
        if position == '先攻':
            debate.user_1 = "ユーザー"
            debate.user_2 = "AI"
        elif position == '後攻':
            debate.user_1 = "AI"
            debate.user_2 = "ユーザー"

        db.session.add(debate)
        db.session.commit()

        if start_button:
            return redirect(url_for('debate.start_debate'))

    # データベースから既存のデータを取得
    debate = AllDebate.query.first()

    return render_template('setting.html', modes=modes, categories=categories, debate=debate)