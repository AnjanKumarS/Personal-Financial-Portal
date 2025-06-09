from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense
from datetime import datetime, timedelta
import random

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/')
@login_required
def index():
    """Display all expenses with optional filtering"""
    # Create sample expenses if none exist
    expenses_exist = Expense.query.filter_by(user_id=current_user.id).first() is not None
    if not expenses_exist:
        create_sample_expenses()
    
    # Get filter parameter
    filter_type = request.args.get('filter', 'all')
    
    # Base query
    query = Expense.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    today = datetime.now()
    if filter_type == 'this_month':
        query = query.filter(
            db.extract('month', Expense.date) == today.month,
            db.extract('year', Expense.date) == today.year
        )
    elif filter_type == 'last_month':
        last_month = today.month - 1 if today.month > 1 else 12
        last_month_year = today.year if today.month > 1 else today.year - 1
        query = query.filter(
            db.extract('month', Expense.date) == last_month,
            db.extract('year', Expense.date) == last_month_year
        )
    elif filter_type == 'this_year':
        query = query.filter(db.extract('year', Expense.date) == today.year)
    
    # Get filtered expenses
    expenses = query.order_by(Expense.date.desc()).all()
    
    # Calculate total amount for filtered expenses
    total_amount = sum(expense.amount for expense in expenses)
    
    # Get expense categories and amounts for chart
    categories = []
    category_amounts = []
    category_totals = {}
    
    for expense in expenses:
        if expense.category in category_totals:
            category_totals[expense.category] += expense.amount
        else:
            category_totals[expense.category] = expense.amount
    
    for category, amount in category_totals.items():
        categories.append(category)
        category_amounts.append(amount)
    
    return render_template('expenses/index.html', 
                          title='Expenses', 
                          expenses=expenses, 
                          total_amount=total_amount,
                          categories=categories,
                          category_amounts=category_amounts,
                          active_filter=filter_type)

@expenses_bp.route('/add', methods=['POST'])
@login_required
def add_expense():
    """Add a new expense"""
    if request.method == 'POST':
        date_str = request.form.get('date')
        category = request.form.get('category')
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        expense = Expense(
            user_id=current_user.id,
            date=date,
            category=category,
            description=description,
            amount=amount
        )
        
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expenses.index'))

@expenses_bp.route('/edit/<int:expense_id>', methods=['POST'])
@login_required
def edit_expense(expense_id):
    """Edit an existing expense"""
    expense = Expense.query.get_or_404(expense_id)
    
    # Verify ownership
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense.', 'danger')
        return redirect(url_for('expenses.index'))
    
    if request.method == 'POST':
        date_str = request.form.get('date')
        category = request.form.get('category')
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        expense.date = date
        expense.category = category
        expense.description = description
        expense.amount = amount
        
        db.session.commit()
        
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expenses.index'))

@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    expense = Expense.query.get_or_404(expense_id)
    
    # Verify ownership
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense.', 'danger')
        return redirect(url_for('expenses.index'))
    
    db.session.delete(expense)
    db.session.commit()
    
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses.index'))

def create_sample_expenses():
    """Create sample expenses for demonstration"""
    categories = ['Housing', 'Transportation', 'Food', 'Utilities', 'Entertainment', 'Healthcare']
    descriptions = {
        'Housing': ['Rent', 'Mortgage Payment', 'Property Tax', 'Home Insurance', 'Home Repairs'],
        'Transportation': ['Car Payment', 'Gas', 'Car Insurance', 'Public Transit', 'Uber/Lyft'],
        'Food': ['Groceries', 'Restaurant', 'Coffee Shop', 'Fast Food', 'Food Delivery'],
        'Utilities': ['Electricity', 'Water', 'Internet', 'Phone Bill', 'Streaming Services'],
        'Entertainment': ['Movies', 'Concert Tickets', 'Video Games', 'Subscription Services', 'Hobbies'],
        'Healthcare': ['Doctor Visit', 'Prescription', 'Health Insurance', 'Gym Membership', 'Dental Care']
    }
    
    # Create expenses for the last 30 days
    for i in range(30, 0, -1):
        date = datetime.now() - timedelta(days=i)
        
        # Add 1-3 expenses per day
        for _ in range(random.randint(1, 3)):
            category = random.choice(categories)
            description = random.choice(descriptions[category])
            
            # Generate realistic amounts based on category
            if category == 'Housing':
                amount = round(random.uniform(500, 2000), 2)
            elif category == 'Transportation':
                amount = round(random.uniform(20, 200), 2)
            elif category == 'Food':
                amount = round(random.uniform(10, 100), 2)
            elif category == 'Utilities':
                amount = round(random.uniform(50, 200), 2)
            elif category == 'Entertainment':
                amount = round(random.uniform(15, 150), 2)
            else:  # Healthcare
                amount = round(random.uniform(20, 300), 2)
            
            expense = Expense(
                user_id=current_user.id,
                date=date,
                category=category,
                description=description,
                amount=amount
            )
            
            db.session.add(expense)
    
    db.session.commit()
    flash('Sample expenses have been created for demonstration purposes.', 'info')
