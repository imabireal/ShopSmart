from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.utils import db_helper
from app.utils import utils

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add_to_cart/<product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Please log in to add items to cart',
            'redirect': url_for('auth.login')
        }), 401

    # Check if product exists (search in both main and seller products)
    product = db_helper.get_product_by_id(product_id)
    
    if not product:
        seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
        for seller in seller_usernames:
            product = db_helper.get_seller_product_by_id(seller, product_id)
            if product:
                break

    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    # Get and clean cart from session
    cart = utils.clean_cart_session()

    # Convert product_id to int and add or update item in cart
    #product_id = int(product_id)
    if product_id in cart:
        cart[product_id] = int(cart[product_id]) + 1
    else:
        cart[product_id] = 1

    # Ensure all keys and values are strictly integers
    cleaned_cart = {}
    for k, v in cart.items():
        try:
            key = int(k) if isinstance(k, (int, str)) else None
            value = int(v) if isinstance(v, (int, str)) else None
            if key is not None and value is not None and key > 0 and value > 0:
                cleaned_cart[key] = value
        except (ValueError, TypeError):
            continue

    session['cart'] = cleaned_cart
    session.modified = True

    # Calculate cart count
    cart_count = sum(cleaned_cart.values())

    return jsonify({
        'success': True,
        'message': f'{product["Description"]} added to cart',
        'cart_count': cart_count
    })

@cart_bp.route('/cart')
@login_required
def cart():
    # Clean and validate cart from session
    cart = utils.clean_cart_session()
    
    cart_items = []
    cart_total = 0
    
    for product_id, quantity in cart.items():
        product = db_helper.get_product_by_id(product_id)

        # If not found in main products, search seller products
        if not product:
            seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
            for seller in seller_usernames:
                product = db_helper.get_seller_product_by_id(seller, product_id)
                if product:
                    break

        if product:
            item_total = product['price_inr'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            cart_total += item_total
    
    # Calculate final total (cart items + buy-now items)
    total = cart_total 
    
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         total=total, 
                         cart_count=sum(cart.values())
                        )

@cart_bp.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 0))

    cart = session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity

    # Clean cart using utils function
    cleaned_cart = utils.clean_cart_session()

    session['cart'] = cleaned_cart
    session.modified = True

    cart_count = sum(cleaned_cart.values())

    return jsonify({'success': True, 'cart_count': cart_count})

@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(product_id, None)
    session['cart'] = cart
    
    cart_count = sum(cart.values())
    
    return jsonify({'success': True, 'cart_count': cart_count})

@cart_bp.route('/buy_now/<int:product_id>')
@login_required
def buy_now(product_id):
    # Check if product exists
    product = db_helper.get_product_by_id(product_id)

    if not product:
        seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
        for seller in seller_usernames:
            product = db_helper.get_seller_product_by_id(seller, product_id)
            if product:
                break

    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('product.home'))

    # Store buy-now item in separate session variable
    session['buy_now_item'] = {
        'product_id': product_id,
        'quantity': 1,
        'product': product
    }
    session.modified = True

    # Redirect to immediate buy-now checkout
    return redirect(url_for('cart.buy_now_checkout'))
