from app import db
from datetime import datetime

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    spent_amount = db.Column(db.Float, nullable=False, default=0.0)
    spent_percentage = db.Column(db.Float, nullable=False, default=0.0)
    
    def __repr__(self):
        return f"Budget('{self.category}', '{self.amount}', '{self.start_date}', '{self.end_date}')"
