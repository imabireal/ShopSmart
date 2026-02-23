from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.utils import db_helper
from app.utils import utils

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/add_to_cart/<product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Please log in to add items to cart',
            'redirect': url_for('auth.login')
        }), 401

    product = db_helper.get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    cart = utils.clean_cart_session()
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    session.modified = True

    cart_count = sum(cart.values())
    return jsonify({
        'success': True,
        'message': f'{product["Description"]} added to cart',
        'cart_count': cart_count
    })


@cart_bp.route('/cart')
@login_required
def cart():
    cart = utils.clean_cart_session()
    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        product = db_helper.get_product_by_id(product_id)
        if product:
            item_total = product['price_inr'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            cart_total += item_total

    return render_template('cart.html',
                         cart_items=cart_items,
                         total=cart_total,
                         cart_count=sum(cart.values()))


@cart_bp.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 0))

    cart = utils.clean_cart_session()

    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity

    session['cart'] = cart
    session.modified = True

    cart_count = sum(cart.values())
    return jsonify({'success': True, 'cart_count': cart_count})


@cart_bp.route('/remove_from_cart/<product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = utils.clean_cart_session()
    cart.pop(product_id, None)
    session['cart'] = cart
    session.modified = True

    cart_count = sum(cart.values())
    return jsonify({'success': True, 'cart_count': cart_count})

@cart_bp.route('/buy_now/<product_id>')
@login_required
def buy_now(product_id):
    # Check if product exists
    product = db_helper.get_product_by_id(product_id)

    if product:
        # Clear any existing buy_now_item from session (no longer needed)
        session.pop('buy_now_item', None)
        session.modified = True
        
        # Redirect directly to buy-now checkout with product_id
        return redirect(url_for('order.buy_now_checkout', product_id=product_id))
    else:
        flash('Product not found. Please select a valid product.', 'error')
        return redirect(url_for('product.home'))
