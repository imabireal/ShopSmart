from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User, Admin, Seller
from app.extensions import login_manager
from app import db_helper

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    # Check if it's an admin
    if user_id.startswith('admin_'):
        username = user_id.replace('admin_', '')
        if username in ['admin', 'superadmin']:
            return Admin(username)
    # Check if it's a seller
    elif user_id.startswith('seller_'):
        username = user_id.replace('seller_', '')
        if username in ['seller1', 'seller2']:
            return Seller(username)
    # Regular user
    else:
        session_user_id = session.get('user_id')
        session_username = session.get('username')
        
        if session_user_id == user_id and session_username:
            return User(session_user_id, session_username)
    
    return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('product.home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        result = db_helper.login_user(username, password)
        
        if result["success"]:
            user_data = result["user"]
            # Create User object for Flask-Login
            user = User(user_data["_id"], user_data["username"])
            login_user(user)
            # Store user_id in session for persistence
            session['user_id'] = user_data["_id"]
            session['username'] = user_data["username"]
            session['role'] = 'customer'
            return redirect(url_for('product.home'))
        else:
            flash(result["message"])
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        result = db_helper.create_user(username, password)
        
        if result["success"]:
            user_data = result["user"]
            # Store user info in session for persistence
            session['user_id'] = user_data["_id"]
            session['username'] = user_data["username"]
            flash('Account created successfully. Please log in.')
            return redirect(url_for('auth.login'))
        else:
            flash(result["message"])
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # Clear user session data
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated and hasattr(current_user, 'role') and current_user.role == 'admin':
        return redirect(url_for('product.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in ['admin', 'superadmin'] and password == 'admin123':
            admin = Admin(username)
            login_user(admin)
            session['user_id'] = f'admin_{username}'
            session['username'] = username
            session['role'] = 'admin'
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('product.admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    
    return render_template('admin_login.html')

@auth_bp.route('/seller/login', methods=['GET', 'POST'])
def seller_login():
    """Seller login page"""
    if current_user.is_authenticated and hasattr(current_user, 'role') and current_user.role == 'seller':
        return redirect(url_for('product.seller_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in ['seller1', 'seller2'] and password == 'seller123':
            seller = Seller(username)
            login_user(seller)
            session['user_id'] = f'seller_{username}'
            session['username'] = username
            session['role'] = 'seller'
            flash('Welcome, Seller!', 'success')
            return redirect(url_for('product.seller_dashboard'))
        else:
            flash('Invalid seller credentials', 'error')
    
    return render_template('seller_login.html')
