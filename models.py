from extensions import db

class AllDebate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, default="")  
    mode = db.Column(db.String(20), nullable=False, default="")  
    topic = db.Column(db.String(200), nullable=False, default="") 
    user_1 = db.Column(db.String(50), nullable=False)
    user_2 = db.Column(db.String(50), nullable=False)
    user_1_claim = db.Column(db.Text, default="")
    user_2_claim = db.Column(db.Text, default="")
    user_1_counter = db.Column(db.Text, default="")
    user_2_counter = db.Column(db.Text, default="")
    user_1_final = db.Column(db.Text, default="")
    user_2_final = db.Column(db.Text, default="")
    feedback = db.Column(db.Text, default="[]")
    winner = db.Column(db.String(50), default="")