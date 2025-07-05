from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from .models import User, Plant

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
    users = User.query.all()
    plants = Plant.query.all()
    return render_template('admin_dashboard.html', users=users, plants=plants)