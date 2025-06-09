from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.user import User
from app import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html', user=current_user)

@profile_bp.route('/settings')
@login_required
def settings():
    return render_template('profile/settings.html', user=current_user) 