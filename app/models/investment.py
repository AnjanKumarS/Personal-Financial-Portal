from app import db
from datetime import datetime

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=False)
    gain_loss = db.Column(db.Float, nullable=False, default=0.0)
    gain_loss_percentage = db.Column(db.Float, nullable=False, default=0.0)
    
    def __repr__(self):
        return f"Investment('{self.name}', '{self.type}', '{self.purchase_date}', '{self.current_value}')"
