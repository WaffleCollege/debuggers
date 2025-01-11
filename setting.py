from flask import Blueprint, request, render_template, redirect, url_for
from extensions import db
from models import AllDebate



# モード選択、カテゴリー選択、ロール選択を一つのBlueprintに
setting_bp = Blueprint('setting', __name__)

#ホーム画面に戻る
@setting_bp.route('/home', methods=['POST'])
def home():
    print("Back to home")
    return redirect(url_for('home'))
#前に戻る
@setting_bp.route('/back', methods=['POST'])
def back():
    print("Back to previous screen")
    return redirect(url_for('home'))

@setting_bp.route('/setting', methods=['GET', 'POST'])
def setting():
    modes = ['やさしい', 'ふつう', 'むずかしい']
    categories = ['環境問題', '教育', '社会問題', 'テクノロジー']

    if request.method == 'POST':
        # POST データをログ出力
        print("Received POST data:", request.form)

        # フォームデータから値を取得
        mode = request.form.get('mode')
        category = request.form.get('category')
        topic = request.form.get('topic')
        position = request.form.get('position')
        start_button = request.form.get('start_button')

        print(f"Mode: {mode}, Category: {category}, Topic: {topic}, Position: {position}")

        # `AllDebate` レコードを取得または作成
        debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
        if not debate:
            debate = AllDebate()

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

    debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
    return render_template('setting.html', modes=modes, categories=categories, debate=debate)