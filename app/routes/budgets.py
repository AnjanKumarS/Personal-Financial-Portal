from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.budget import Budget
from datetime import datetime, timedelta
import random

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@budgets_bp.route('/')
@login_required
def index():
    """Display all budgets with optional filtering"""
    # Create sample budgets if none exist
    budgets_exist = Budget.query.filter_by(user_id=current_user.id).first() is not None
    if not budgets_exist:
        create_sample_budgets()
    
    # Get filter parameter
    filter_type = request.args.get('filter', 'all')
    
    # Base query
    query = Budget.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    today = datetime.now().date()
    if filter_type == 'active':
        query = query.filter(
            Budget.start_date <= today,
            Budget.end_date >= today
        )
    elif filter_type == 'completed':
        query = query.filter(Budget.end_date < today)
    
    # Get filtered budgets
    budgets = query.all()
    
    # Calculate totals for filtered budgets
    total_budget = sum(budget.amount for budget in budgets)
    total_spent = sum(budget.spent_amount for budget in budgets)
    
    # Get budget categories and amounts for chart
    categories = []
    budget_amounts = []
    spent_amounts = []
    
    for budget in budgets:
        categories.append(budget.category)
        budget_amounts.append(budget.amount)
        spent_amounts.append(budget.spent_amount)
    
    return render_template('budgets/index.html', 
                          title='Budgets', 
                          budgets=budgets, 
                          total_budget=total_budget,
                          total_spent=total_spent,
                          categories=categories,
                          budget_amounts=budget_amounts,
                          spent_amounts=spent_amounts,
                          active_filter=filter_type)

@budgets_bp.route('/add', methods=['POST'])
@login_required
def add_budget():
    """Add a new budget"""
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        budget = Budget(
            user_id=current_user.id,
            category=category,
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            spent_amount=0.0
        )
        
        db.session.add(budget)
        db.session.commit()
        
        flash('Budget created successfully!', 'success')
        return redirect(url_for('budgets.index'))

@budgets_bp.route('/edit/<int:budget_id>', methods=['POST'])
@login_required
def edit_budget(budget_id):
    """Edit an existing budget"""
    budget = Budget.query.get_or_404(budget_id)
    
    # Verify ownership
    if budget.user_id != current_user.id:
        flash('You do not have permission to edit this budget.', 'danger')
        return redirect(url_for('budgets.index'))
    
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        spent_amount = float(request.form.get('spent_amount', budget.spent_amount))
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        budget.category = category
        budget.amount = amount
        budget.start_date = start_date
        budget.end_date = end_date
        budget.spent_amount = spent_amount
        
        # Recalculate spent percentage
        budget.spent_percentage = round((spent_amount / amount) * 100, 1) if amount > 0 else 0
        
        db.session.commit()
        
        flash('Budget updated successfully!', 'success')
        return redirect(url_for('budgets.index'))

@budgets_bp.route('/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    """Delete a budget"""
    budget = Budget.query.get_or_404(budget_id)
    
    # Verify ownership
    if budget.user_id != current_user.id:
        flash('You do not have permission to delete this budget.', 'danger')
        return redirect(url_for('budgets.index'))
    
    db.session.delete(budget)
    db.session.commit()
    
    flash('Budget deleted successfully!', 'success')
    return redirect(url_for('budgets.index'))

def create_sample_budgets():
    """Create sample budgets for demonstration"""
    categories = ['Housing', 'Transportation', 'Food', 'Utilities', 'Entertainment', 'Healthcare']
    
    # Current month start and end dates
    today = datetime.now()
    start_date = datetime(today.year, today.month, 1)
    if today.month == 12:
        end_date = datetime(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    
    # Create budget for each category
    for category in categories:
        # Set realistic budget amounts based on category
        if category == 'Housing':
            amount = 1500.00
            spent = round(random.uniform(1000, 1500), 2)
        elif category == 'Transportation':
            amount = 400.00
            spent = round(random.uniform(250, 400), 2)
        elif category == 'Food':
            amount = 600.00
            spent = round(random.uniform(400, 600), 2)
        elif category == 'Utilities':
            amount = 300.00
            spent = round(random.uniform(200, 300), 2)
        elif category == 'Entertainment':
            amount = 200.00
            spent = round(random.uniform(100, 250), 2)
        else:  # Healthcare
            amount = 250.00
            spent = round(random.uniform(50, 200), 2)
        
        # Calculate spent percentage
        spent_percentage = round((spent / amount) * 100, 1)
        
        budget = Budget(
            user_id=current_user.id,
            category=category,
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            spent_amount=spent,
            spent_percentage=spent_percentage
        )
        
        db.session.add(budget)
    
    db.session.commit()
    flash('Sample budgets have been created for demonstration purposes.', 'info')
