from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Redirect to dashboard if logged in, otherwise to login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))
