from flask import Flask, redirect, url_for
from extensions import db
from models import AllDebate
from mode import mode_bp
from category import category_bp
from debate import debate_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ブループリントの登録
app.register_blueprint(mode_bp)
app.register_blueprint(category_bp)
app.register_blueprint(debate_bp)

@app.route('/')
def home():
    return redirect(url_for('mode.mode_selection'))

with app.app_context():
    db.create_all()

    # 初期データの挿入
    if not AllDebate.query.first():
        initial_data = AllDebate(
            user_1="ユーザー",
            user_2="AI",
            mode="やさしい",
            category="環境問題",
            topic="環境問題について",
            feedback="[]"
        )
        db.session.add(initial_data)
        db.session.commit()
        print("初期データを作成しました。")

if __name__ == "__main__":
    app.run(debug=True)
