from app import create_app, db
from app.models.user import User
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.investment import Investment
from app.models.bill import Bill

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Add database and models to flask shell context"""
    return {
        'db': db, 
        'User': User, 
        'Expense': Expense, 
        'Budget': Budget, 
        'Investment': Investment, 
        'Bill': Bill
    }

if __name__ == '__main__':
    app.run(debug=True, port=5002, host="0.0.0.0")
