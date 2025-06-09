from flask import Blueprint, redirect, url_for

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')
budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')
investments_bp = Blueprint('investments', __name__, url_prefix='/investments')
bills_bp = Blueprint('bills', __name__, url_prefix='/bills')

# Create a main blueprint for root routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Redirect root URL to login page"""
    return redirect(url_for('auth.login'))
