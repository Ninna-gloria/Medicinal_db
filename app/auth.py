from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, AuthLog
from . import db
import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            log_auth_action(user.id, 'login')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    log_auth_action(current_user.id, 'logout')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, password_hash=generate_password_hash(password), email=email)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

def log_auth_action(user_id, action):
    auth_log = AuthLog(user_id=user_id, action=action, timestamp=datetime.datetime.utcnow())
    db.session.add(auth_log)
    db.session.commit()