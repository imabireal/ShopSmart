from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User, AdminSeller
from app.extensions import login_manager
from app.utils import db_helper

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    # Check if it's an admin_seller
    if user_id.startswith('admin_seller_'):
        username = user_id.replace('admin_seller_', '')
        admin_seller_data = db_helper.get_admin_seller_by_username(username)
        if admin_seller_data:
            return AdminSeller(admin_seller_data["username"], admin_seller_data["role"])
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

@auth_bp.route('/admin_seller/login', methods=['GET', 'POST'])
def admin_seller_login():
    """Admin/Seller login page"""
    if current_user.is_authenticated and hasattr(current_user, 'role') and current_user.role in ['admin', 'seller']:
        return redirect(url_for('product.admin_seller_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = db_helper.login_admin_seller(username, password)
        
        if result["success"]:
            admin_seller_data = result["admin_seller"]
            admin_seller = AdminSeller(admin_seller_data["username"], admin_seller_data["role"])
            login_user(admin_seller)
            session['user_id'] = f'admin_seller_{admin_seller_data["username"]}'
            session['username'] = admin_seller_data["username"]
            session['role'] = admin_seller_data["role"]
            
            if admin_seller_data["role"] == 'admin':
                flash('Welcome, Admin!', 'success')
            else:
                flash('Welcome, Seller!', 'success')
                
            return redirect(url_for('product.admin_seller_dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('admin_seller_login.html')
