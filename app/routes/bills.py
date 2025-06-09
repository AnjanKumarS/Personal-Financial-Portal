from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.bill import Bill
from datetime import datetime, timedelta
import random

bills_bp = Blueprint('bills', __name__, url_prefix='/bills')

@bills_bp.route('/')
@login_required
def index():
    """Display all bills with optional filtering"""
    # Create sample bills if none exist
    bills_exist = Bill.query.filter_by(user_id=current_user.id).first() is not None
    if not bills_exist:
        create_sample_bills()
    
    # Get filter parameter
    filter_type = request.args.get('filter', 'all')
    
    # Base query
    query = Bill.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if filter_type == 'upcoming':
        query = query.filter(Bill.status == 'Upcoming')
    elif filter_type == 'paid':
        query = query.filter(Bill.status == 'Paid')
    elif filter_type == 'overdue':
        query = query.filter(Bill.status == 'Overdue')
    
    # Get filtered bills
    bills = query.all()
    
    # Calculate counts and totals
    today = datetime.now().date()
    upcoming_count = 0
    overdue_count = 0
    total_due_month = 0
    
    # Get bill categories and amounts for chart
    bill_categories = []
    category_amounts = []
    category_totals = {}
    
    for bill in bills:
        # Count upcoming bills (due in next 7 days)
        if bill.status != 'Paid' and (bill.due_date.date() - today).days <= 7 and (bill.due_date.date() - today).days >= 0:
            upcoming_count += 1
        
        # Count overdue bills
        if bill.status == 'Overdue':
            overdue_count += 1
        
        # Sum bills due this month
        if bill.due_date.year == today.year and bill.due_date.month == today.month:
            total_due_month += bill.amount
        
        # Categorize for chart
        if bill.category in category_totals:
            category_totals[bill.category] += bill.amount
        else:
            category_totals[bill.category] = bill.amount
    
    for category, amount in category_totals.items():
        bill_categories.append(category)
        category_amounts.append(amount)
    
    return render_template('bills/index.html', 
                          title='Bills', 
                          bills=bills, 
                          upcoming_count=upcoming_count,
                          overdue_count=overdue_count,
                          total_due_month=total_due_month,
                          bill_categories=bill_categories,
                          category_amounts=category_amounts,
                          active_filter=filter_type)

@bills_bp.route('/add', methods=['POST'])
@login_required
def add_bill():
    """Add a new bill"""
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        due_date_str = request.form.get('due_date')
        is_recurring = 'is_recurring' in request.form
        recurrence_frequency = request.form.get('recurrence_frequency') if is_recurring else None
        
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        # Determine status based on due date
        today = datetime.now().date()
        if due_date.date() < today:
            status = 'Overdue'
        else:
            status = 'Upcoming'
        
        bill = Bill(
            user_id=current_user.id,
            name=name,
            category=category,
            amount=amount,
            due_date=due_date,
            status=status,
            is_recurring=is_recurring,
            recurrence_frequency=recurrence_frequency
        )
        
        db.session.add(bill)
        db.session.commit()
        
        flash('Bill added successfully!', 'success')
        return redirect(url_for('bills.index'))

@bills_bp.route('/edit/<int:bill_id>', methods=['POST'])
@login_required
def edit_bill(bill_id):
    """Edit an existing bill"""
    bill = Bill.query.get_or_404(bill_id)
    
    # Verify ownership
    if bill.user_id != current_user.id:
        flash('You do not have permission to edit this bill.', 'danger')
        return redirect(url_for('bills.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        due_date_str = request.form.get('due_date')
        is_recurring = 'is_recurring' in request.form
        recurrence_frequency = request.form.get('recurrence_frequency') if is_recurring else None
        status = request.form.get('status', bill.status)
        
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        # Update bill details
        bill.name = name
        bill.category = category
        bill.amount = amount
        bill.due_date = due_date
        bill.is_recurring = is_recurring
        bill.recurrence_frequency = recurrence_frequency
        bill.status = status
        
        db.session.commit()
        
        flash('Bill updated successfully!', 'success')
        return redirect(url_for('bills.index'))

@bills_bp.route('/delete/<int:bill_id>', methods=['POST'])
@login_required
def delete_bill(bill_id):
    """Delete a bill"""
    bill = Bill.query.get_or_404(bill_id)
    
    # Verify ownership
    if bill.user_id != current_user.id:
        flash('You do not have permission to delete this bill.', 'danger')
        return redirect(url_for('bills.index'))
    
    db.session.delete(bill)
    db.session.commit()
    
    flash('Bill deleted successfully!', 'success')
    return redirect(url_for('bills.index'))

@bills_bp.route('/mark_paid/<int:bill_id>', methods=['POST'])
@login_required
def mark_paid(bill_id):
    """Mark a bill as paid"""
    bill = Bill.query.get_or_404(bill_id)
    
    if bill.user_id != current_user.id:
        flash('You do not have permission to update this bill.', 'danger')
        return redirect(url_for('bills.index'))
    
    bill.status = 'Paid'
    db.session.commit()
    
    flash('Bill marked as paid!', 'success')
    return redirect(url_for('bills.index'))

def create_sample_bills():
    """Create sample bills for demonstration"""
    bills_data = [
        {
            'name': 'Rent',
            'category': 'Rent/Mortgage',
            'amount': 1500.00,
            'days_offset': 5,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Electricity',
            'category': 'Utilities',
            'amount': 120.50,
            'days_offset': -2,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Water',
            'category': 'Utilities',
            'amount': 45.75,
            'days_offset': 10,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Internet',
            'category': 'Utilities',
            'amount': 79.99,
            'days_offset': 15,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Cell Phone',
            'category': 'Phone',
            'amount': 85.00,
            'days_offset': 8,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Car Insurance',
            'category': 'Insurance',
            'amount': 150.00,
            'days_offset': 20,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Health Insurance',
            'category': 'Insurance',
            'amount': 250.00,
            'days_offset': 1,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Netflix',
            'category': 'Subscription',
            'amount': 14.99,
            'days_offset': 12,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Spotify',
            'category': 'Subscription',
            'amount': 9.99,
            'days_offset': 18,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Credit Card Payment',
            'category': 'Credit Card',
            'amount': 350.00,
            'days_offset': -5,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Student Loan',
            'category': 'Loan',
            'amount': 220.00,
            'days_offset': 3,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        },
        {
            'name': 'Car Payment',
            'category': 'Loan',
            'amount': 325.00,
            'days_offset': 7,
            'is_recurring': True,
            'recurrence_frequency': 'Monthly'
        }
    ]
    
    today = datetime.now()
    
    for bill_data in bills_data:
        due_date = today + timedelta(days=bill_data['days_offset'])
        
        # Determine status based on due date
        if due_date.date() < today.date():
            status = 'Overdue'
        else:
            status = 'Upcoming'
        
        # Randomly mark some bills as paid
        if random.random() < 0.3:
            status = 'Paid'
        
        bill = Bill(
            user_id=current_user.id,
            name=bill_data['name'],
            category=bill_data['category'],
            amount=bill_data['amount'],
            due_date=due_date,
            status=status,
            is_recurring=bill_data['is_recurring'],
            recurrence_frequency=bill_data['recurrence_frequency']
        )
        
        db.session.add(bill)
    
    db.session.commit()
    flash('Sample bills have been created for demonstration purposes.', 'info')
