from datetime import datetime

def format_date(date):
    """Format date as string"""
    return date.strftime('%Y-%m-%d')

def format_currency(amount):
    """Format amount as currency string"""
    return f"₹{amount:.2f}"

def get_month_name(month_number):
    """Get month name from month number"""
    return datetime(2000, month_number, 1).strftime('%B')

def get_current_datetime():
    """Get current datetime for templates"""
    return datetime.now()
