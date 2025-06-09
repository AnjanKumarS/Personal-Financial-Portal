from app import db
from datetime import datetime

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Upcoming')  # Upcoming, Paid, Overdue
    is_recurring = db.Column(db.Boolean, nullable=False, default=False)
    recurrence_frequency = db.Column(db.String(20), nullable=True)  # Weekly, Monthly, Quarterly, Yearly
    
    def __repr__(self):
        return f"Bill('{self.name}', '{self.category}', '{self.amount}', '{self.due_date}', '{self.status}')"
