from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.investment import Investment
from datetime import datetime, timedelta
import random

investments_bp = Blueprint('investments', __name__, url_prefix='/investments')

@investments_bp.route('/')
@login_required
def index():
    """Display all investments with optional filtering"""
    # Create sample investments if none exist
    investments_exist = Investment.query.filter_by(user_id=current_user.id).first() is not None
    if not investments_exist:
        create_sample_investments()
    
    # Get filter parameter
    filter_type = request.args.get('filter', 'all')
    
    # Base query
    query = Investment.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if filter_type != 'all' and filter_type in ['Stock', 'Bond', 'Mutual Fund', 'ETF', 'Real Estate', 'Cryptocurrency']:
        query = query.filter(Investment.type == filter_type)
    
    # Get filtered investments
    investments = query.all()
    
    # Calculate totals for filtered investments
    total_invested = sum(investment.purchase_price * investment.quantity for investment in investments)
    total_current_value = sum(investment.current_value for investment in investments)
    total_gain_loss = total_current_value - total_invested
    total_gain_loss_percentage = (total_gain_loss / total_invested * 100) if total_invested > 0 else 0
    
    # Get investment types and values for chart
    investment_types = []
    type_values = []
    type_totals = {}
    
    for investment in investments:
        if investment.type in type_totals:
            type_totals[investment.type] += investment.current_value
        else:
            type_totals[investment.type] = investment.current_value
    
    for inv_type, value in type_totals.items():
        investment_types.append(inv_type)
        type_values.append(value)
    
    # Generate performance data for chart (last 12 months)
    performance_dates = []
    performance_values = []
    
    for i in range(12, 0, -1):
        date = datetime.now() - timedelta(days=i*30)
        performance_dates.append(date.strftime('%b %Y'))
        
        # Generate a somewhat realistic growth curve
        factor = 1 + (i * 0.005) + (random.uniform(-0.02, 0.03))
        value = total_current_value * factor
        performance_values.append(round(value, 2))
    
    # Add current month
    performance_dates.append(datetime.now().strftime('%b %Y'))
    performance_values.append(round(total_current_value, 2))
    
    return render_template('investments/index.html', 
                          title='Investments', 
                          investments=investments, 
                          total_invested=total_invested,
                          total_current_value=total_current_value,
                          total_gain_loss=total_gain_loss,
                          total_gain_loss_percentage=total_gain_loss_percentage,
                          investment_types=investment_types,
                          type_values=type_values,
                          performance_dates=performance_dates,
                          performance_values=performance_values,
                          active_filter=filter_type)

@investments_bp.route('/add', methods=['POST'])
@login_required
def add_investment():
    """Add a new investment"""
    if request.method == 'POST':
        name = request.form.get('name')
        inv_type = request.form.get('type')
        purchase_date_str = request.form.get('purchase_date')
        purchase_price = float(request.form.get('purchase_price'))
        quantity = float(request.form.get('quantity'))
        current_value = float(request.form.get('current_value'))
        
        purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d')
        
        # Calculate gain/loss
        total_purchase = purchase_price * quantity
        gain_loss = current_value - total_purchase
        gain_loss_percentage = (gain_loss / total_purchase * 100) if total_purchase > 0 else 0
        
        investment = Investment(
            user_id=current_user.id,
            name=name,
            type=inv_type,
            purchase_date=purchase_date,
            purchase_price=purchase_price,
            quantity=quantity,
            current_value=current_value,
            gain_loss=gain_loss,
            gain_loss_percentage=gain_loss_percentage
        )
        
        db.session.add(investment)
        db.session.commit()
        
        flash('Investment added successfully!', 'success')
        return redirect(url_for('investments.index'))

@investments_bp.route('/edit/<int:investment_id>', methods=['POST'])
@login_required
def edit_investment(investment_id):
    """Edit an existing investment"""
    investment = Investment.query.get_or_404(investment_id)
    
    # Verify ownership
    if investment.user_id != current_user.id:
        flash('You do not have permission to edit this investment.', 'danger')
        return redirect(url_for('investments.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        inv_type = request.form.get('type')
        purchase_date_str = request.form.get('purchase_date')
        purchase_price = float(request.form.get('purchase_price'))
        quantity = float(request.form.get('quantity'))
        current_value = float(request.form.get('current_value'))
        
        purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d')
        
        # Calculate gain/loss
        total_purchase = purchase_price * quantity
        gain_loss = current_value - total_purchase
        gain_loss_percentage = (gain_loss / total_purchase * 100) if total_purchase > 0 else 0
        
        investment.name = name
        investment.type = inv_type
        investment.purchase_date = purchase_date
        investment.purchase_price = purchase_price
        investment.quantity = quantity
        investment.current_value = current_value
        investment.gain_loss = gain_loss
        investment.gain_loss_percentage = gain_loss_percentage
        
        db.session.commit()
        
        flash('Investment updated successfully!', 'success')
        return redirect(url_for('investments.index'))

@investments_bp.route('/delete/<int:investment_id>', methods=['POST'])
@login_required
def delete_investment(investment_id):
    """Delete an investment"""
    investment = Investment.query.get_or_404(investment_id)
    
    # Verify ownership
    if investment.user_id != current_user.id:
        flash('You do not have permission to delete this investment.', 'danger')
        return redirect(url_for('investments.index'))
    
    db.session.delete(investment)
    db.session.commit()
    
    flash('Investment deleted successfully!', 'success')
    return redirect(url_for('investments.index'))

def create_sample_investments():
    """Create sample investments for demonstration"""
    investments_data = [
        {
            'name': 'Apple Inc.',
            'type': 'Stock',
            'purchase_price': 150.75,
            'quantity': 10,
            'current_value': 1750.50,
            'days_ago': 365
        },
        {
            'name': 'Microsoft Corp.',
            'type': 'Stock',
            'purchase_price': 245.30,
            'quantity': 5,
            'current_value': 1350.25,
            'days_ago': 180
        },
        {
            'name': 'Vanguard Total Stock Market ETF',
            'type': 'ETF',
            'purchase_price': 205.80,
            'quantity': 15,
            'current_value': 3300.75,
            'days_ago': 730
        },
        {
            'name': 'US Treasury Bond',
            'type': 'Bond',
            'purchase_price': 1000.00,
            'quantity': 3,
            'current_value': 3150.00,
            'days_ago': 1095
        },
        {
            'name': 'Fidelity Growth Fund',
            'type': 'Mutual Fund',
            'purchase_price': 55.25,
            'quantity': 100,
            'current_value': 6250.50,
            'days_ago': 545
        },
        {
            'name': 'Bitcoin',
            'type': 'Cryptocurrency',
            'purchase_price': 35000.00,
            'quantity': 0.15,
            'current_value': 6750.00,
            'days_ago': 90
        },
        {
            'name': 'Rental Property',
            'type': 'Real Estate',
            'purchase_price': 250000.00,
            'quantity': 1,
            'current_value': 285000.00,
            'days_ago': 1825
        }
    ]
    
    for inv_data in investments_data:
        purchase_date = datetime.now() - timedelta(days=inv_data['days_ago'])
        
        # Calculate gain/loss
        total_purchase = inv_data['purchase_price'] * inv_data['quantity']
        gain_loss = inv_data['current_value'] - total_purchase
        gain_loss_percentage = (gain_loss / total_purchase * 100) if total_purchase > 0 else 0
        
        investment = Investment(
            user_id=current_user.id,
            name=inv_data['name'],
            type=inv_data['type'],
            purchase_date=purchase_date,
            purchase_price=inv_data['purchase_price'],
            quantity=inv_data['quantity'],
            current_value=inv_data['current_value'],
            gain_loss=gain_loss,
            gain_loss_percentage=gain_loss_percentage
        )
        
        db.session.add(investment)
    
    db.session.commit()
    flash('Sample investments have been created for demonstration purposes.', 'info')
