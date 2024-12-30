from flask import Flask
from extensions import db
from mode import mode_bp
from category import category_bp
from debate import debate_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # データベース初期化
    db.init_app(app)

    # Blueprint の登録
    app.register_blueprint(mode_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(debate_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # データベーステーブルを作成
    app.run(debug=True)
