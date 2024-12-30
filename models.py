
from extensions import db

class AllDebate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_1 = db.Column(db.String(50), nullable=False)
    user_2 = db.Column(db.String(50), nullable=False)
    mode = db.Column(db.String(20), nullable=True)  # 追加: nullable=True
    category = db.Column(db.String(50), nullable=True)  # 追加: nullable=True
    topic = db.Column(db.String(200), nullable=True)  # 追加: nullable=True
    user_1_claim = db.Column(db.Text, default="")
    user_2_claim = db.Column(db.Text, default="")
    user_1_counter = db.Column(db.Text, default="")
    user_2_counter = db.Column(db.Text, default="")
    user_1_final = db.Column(db.Text, default="")
    user_2_final = db.Column(db.Text, default="")
    feedback = db.Column(db.Text, default="[]")  # 空のJSONリストとして初期化
    winner = db.Column(db.String(50), default="")