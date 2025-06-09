from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.investment import Investment
from app.models.bill import Bill
from datetime import datetime, timedelta
import random

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Redirect to dashboard if logged in, otherwise to login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """Display dashboard with summary of all financial data"""
    # Get expenses data
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Get all expenses for the current month
    month_expenses = Expense.query.filter_by(user_id=current_user.id).filter(
        db.extract('month', Expense.date) == current_month,
        db.extract('year', Expense.date) == current_year
    ).all()
    
    # Calculate total expenses for current month
    total_expenses = sum(expense.amount for expense in month_expenses) if month_expenses else 0
    
    # Get recent expenses for display
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).limit(5).all()
    
    # Get expense categories and amounts for chart
    all_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    expense_categories = []
    expense_amounts = []
    category_totals = {}
    
    for expense in all_expenses:
        if expense.category in category_totals:
            category_totals[expense.category] += expense.amount
        else:
            category_totals[expense.category] = expense.amount
    
    for category, amount in category_totals.items():
        expense_categories.append(category)
        expense_amounts.append(amount)
    
    # Get budgets data
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    total_budget = sum(budget.amount for budget in budgets) if budgets else 0
    total_spent = sum(budget.spent_amount for budget in budgets) if budgets else 0
    
    # Get budget categories and amounts for chart
    budget_categories = []
    budget_amounts = []
    spent_amounts = []
    
    for budget in budgets:
        budget_categories.append(budget.category)
        budget_amounts.append(budget.amount)
        spent_amounts.append(budget.spent_amount)
    
    # Get investments data
    investments = Investment.query.filter_by(user_id=current_user.id).all()
    total_invested = sum(investment.purchase_price * investment.quantity for investment in investments) if investments else 0
    total_current_value = sum(investment.current_value for investment in investments) if investments else 0
    
    # Get bills data
    today = datetime.now().date()
    bills = Bill.query.filter_by(user_id=current_user.id).all()
    
    # Count upcoming bills (due in next 7 days)
    upcoming_bills = [bill for bill in bills if bill.status != 'Paid' and 
                     (bill.due_date.date() - today).days <= 7 and 
                     (bill.due_date.date() - today).days >= 0]
    upcoming_count = len(upcoming_bills)
    
    # Count overdue bills
    overdue_bills = [bill for bill in bills if bill.status == 'Overdue']
    overdue_count = len(overdue_bills)
    
    # Sum bills due this month
    current_month_bills = [bill for bill in bills if bill.due_date.year == today.year and 
                          bill.due_date.month == today.month]
    total_due_month = sum(bill.amount for bill in current_month_bills)
    
    return render_template('dashboard/index.html', 
                          title='Dashboard',
                          expenses=expenses,
                          total_expenses=total_expenses,
                          expense_categories=expense_categories,
                          expense_amounts=expense_amounts,
                          budgets=budgets,
                          total_budget=total_budget,
                          total_spent=total_spent,
                          budget_categories=budget_categories,
                          budget_amounts=budget_amounts,
                          spent_amounts=spent_amounts,
                          investments=investments,
                          total_invested=total_invested,
                          total_current_value=total_current_value,
                          upcoming_bills=upcoming_bills,
                          upcoming_count=upcoming_count,
                          overdue_count=overdue_count,
                          total_due_month=total_due_month)
