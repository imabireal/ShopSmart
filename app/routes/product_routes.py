from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.utils import db_helper
from app.utils import utils

product_bp = Blueprint('product', __name__)

@product_bp.before_request
def before_request():
    """Clean session before each request to prevent serialization errors"""
    try:
        # Clean cart data
        utils.clean_cart_session()
        # Clean buy-now item data
        utils.clean_buy_now_session()
    except Exception as e:
        # If cleaning fails, reset entire session
        utils.reset_session()

@product_bp.route('/')
def home():
    # Clean and validate cart from session
    cart = utils.clean_cart_session()
    cart_count = sum(cart.values()) if cart else 0

    # Pagination configuration
    ITEMS_PER_PAGE = 12  # Can be adjusted to 20 as needed
    
    # Get current page from query parameter, default to 1
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    # Get paginated main products
    all_products = db_helper.get_products_paginated(page=page, per_page=ITEMS_PER_PAGE)
    
    # Get paginated seller products
    seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
    for seller in seller_usernames:
        seller_products = db_helper.get_seller_products_paginated(seller, page=page, per_page=ITEMS_PER_PAGE)
        for product in seller_products:
            all_products.append({
                **product,
                'seller': seller
            })
    
    # Calculate pagination metadata
    main_products_count = db_helper.count_products()
    total_seller_products = sum(db_helper.count_seller_products(seller) for seller in seller_usernames)
    total_products = main_products_count + total_seller_products
    total_pages = (total_products + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE  # Ceiling division
    
    # Ensure page doesn't exceed total pages
    if page > total_pages and total_pages > 0:
        page = total_pages
        # Refetch products for the corrected page
        all_products = db_helper.get_products_paginated(page=page, per_page=ITEMS_PER_PAGE)
        for seller in seller_usernames:
            seller_products = db_helper.get_seller_products_paginated(seller, page=page, per_page=ITEMS_PER_PAGE)
            for product in seller_products:
                all_products.append({
                    **product,
                    'seller': seller
                })
    
    # Pagination metadata for template
    pagination = {
        'current_page': page,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'items_per_page': ITEMS_PER_PAGE,
        'total_items': total_products
    }

    return render_template('home.html', 
                           products=all_products, 
                           cart=cart, 
                           cart_count=cart_count, 
                           current_user=current_user,
                           pagination=pagination)

@product_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard - can manage all products"""
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('product.home'))

    all_products = db_helper.get_products()

    # Add seller products info
    seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
    seller_products = {}
    for seller in seller_usernames:
        seller_prods = db_helper.get_seller_products(seller)
        seller_products[seller] = seller_prods
        for product in seller_prods:
            all_products.append({
                **product,
                'seller': seller,
                'is_seller_product': True
            })

    return render_template('admin_dashboard.html', products=all_products, seller_products=seller_products)

@product_bp.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    """Admin can add new products to main catalog"""
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('product.home'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])

        new_product = db_helper.add_product(name, price)

        flash(f'Product "{name}" added successfully!', 'success')
        return redirect(url_for('product.admin_dashboard'))
    
    return render_template('admin_add_product.html')

@product_bp.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(product_id):
    """Admin can edit any product"""
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('product.home'))

    # Find product in main catalog
    product = db_helper.get_product_by_id(product_id)

    # If not found, check seller products
    is_seller_product = False
    seller_username = None
    if not product:
        seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
        for seller in seller_usernames:
            product = db_helper.get_seller_product_by_id(seller, product_id)
            if product:
                product['seller'] = seller
                is_seller_product = True
                seller_username = seller
                break

    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('product.admin_dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])

        if is_seller_product:
            db_helper.update_seller_product(seller_username, product_id, name, price)
        else:
            db_helper.update_product(product_id, name, price)

        flash(f'Product "{name}" updated successfully!', 'success')
        return redirect(url_for('product.admin_dashboard'))

    return render_template('admin_edit_product.html', product=product, is_seller_product=is_seller_product)

@product_bp.route('/admin/delete_product/<int:product_id>')
@login_required
def admin_delete_product(product_id):
    """Admin can delete any product"""
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('product.home'))

    # Try to delete from main products first
    if db_helper.delete_product(product_id):
        flash('Product deleted successfully!', 'success')
    else:
        # Check seller products
        seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
        for seller in seller_usernames:
            if db_helper.delete_seller_product(seller, product_id):
                flash('Seller product deleted successfully!', 'success')
                break
        else:
            flash('Product not found', 'error')

    return redirect(url_for('product.admin_dashboard'))

@product_bp.route('/seller/dashboard')
@login_required
def seller_dashboard():
    """Seller dashboard - can only manage their own products"""
    if not hasattr(current_user, 'role') or current_user.role != 'seller':
        flash('Access denied. Seller only.', 'error')
        return redirect(url_for('product.home'))

    seller_name = current_user.username
    my_products = db_helper.get_seller_products(seller_name)

    return render_template('seller_dashboard.html', products=my_products, seller_name=seller_name)

@product_bp.route('/seller/add_product', methods=['GET', 'POST'])
@login_required
def seller_add_product():
    """Seller can add their own products"""
    if not hasattr(current_user, 'role') or current_user.role != 'seller':
        flash('Access denied. Seller only.', 'error')
        return redirect(url_for('product.home'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        
        seller_name = current_user.username
        new_product = db_helper.add_seller_product(seller_name, name, price)
        
        flash(f'Product "{name}" added successfully!', 'success')
        return redirect(url_for('product.seller_dashboard'))
    
    return render_template('seller_add_product.html')

@product_bp.route('/seller/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def seller_edit_product(product_id):
    """Seller can only edit their own products"""
    if not hasattr(current_user, 'role') or current_user.role != 'seller':
        flash('Access denied. Seller only.', 'error')
        return redirect(url_for('product.home'))

    seller_name = current_user.username
    product = db_helper.get_seller_product_by_id(seller_name, product_id)

    if not product:
        flash('Product not found or you do not have permission to edit it', 'error')
        return redirect(url_for('product.seller_dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])

        db_helper.update_seller_product(seller_name, product_id, name, price)

        flash(f'Product "{name}" updated successfully!', 'success')
        return redirect(url_for('product.seller_dashboard'))

    return render_template('seller_edit_product.html', product=product)

@product_bp.route('/seller/delete_product/<int:product_id>')
@login_required
def seller_delete_product(product_id):
    """Seller can only delete their own products"""
    if not hasattr(current_user, 'role') or current_user.role != 'seller':
        flash('Access denied. Seller only.', 'error')
        return redirect(url_for('product.home'))

    seller_name = current_user.username

    if db_helper.delete_seller_product(seller_name, product_id):
        flash('Product deleted successfully!', 'success')
    else:
        flash('Product not found or you do not have permission to delete it', 'error')

    return redirect(url_for('product.seller_dashboard'))
