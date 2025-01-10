from flask import Flask, redirect, url_for,render_template
from extensions import db
from models import AllDebate
from debate import debate_bp
from flask_migrate import Migrate
from setting import setting_bp# setting_bpのインポートを追加


# Flask アプリケーションの初期化
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの初期化
db.init_app(app)

# Flask-Migrate の初期化
migrate = Migrate(app, db)

# ブループリントの登録
app.register_blueprint(debate_bp)
app.register_blueprint(setting_bp)

@app.route('/')
def home():
    """ルートURLにアクセスした際に設定画面にリダイレクト 一旦設定画面です"""
    return redirect(url_for('setting.setting'))

# アプリケーションコンテキスト内で初期設定
with app.app_context():
    db.create_all()  # データベースのテーブルを作成
    if AllDebate.query.first() is None:
        # 初期データを挿入
        initial_data = AllDebate(
            user_1="ユーザー",
            user_2="AI",
            category="テクノロジー",
            role = "先攻",
            topic="テクノロジーについて",
            feedback="[]",
            user_input_count=0,  # デフォルト値
        )
        db.session.add(initial_data)
        db.session.commit()
        print("初期データが追加されました。")

if __name__ == "__main__":
    app.run(debug=True)



