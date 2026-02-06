from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from flask_login import login_required
from app.utils import db_helper
import app.utils.utils as utils

order_bp = Blueprint('order', __name__)

@order_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    buy_now_item = session.get('buy_now_item')

    # Check if there's something to checkout
    if not cart and not buy_now_item:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart.cart'))

    # Get checkout data
    name = request.form.get('name', '').strip()
    address = request.form.get('address', '').strip()
    card_number = request.form.get('card_number', '').strip()
    expiry_date = request.form.get('expiry_date', '').strip()
    cvv = request.form.get('cvv', '').strip()

    # Validate required fields
    if not all([name, address, card_number, expiry_date, cvv]):
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('cart.cart'))

    # Basic card number validation (demo purposes)
    if len(card_number.replace(' ', '')) < 13:
        flash('Invalid card number', 'error')
        return redirect(url_for('cart.cart'))

    # Basic expiry date validation
    try:
        month, year = expiry_date.split('/')
        if int(month) < 1 or int(month) > 12:
            raise ValueError('Invalid month')
    except:
        flash('Invalid expiry date format (MM/YY)', 'error')
        return redirect(url_for('cart.cart'))

    # Basic CVV validation
    if len(cvv) < 3:
        flash('Invalid CVV', 'error')
        return redirect(url_for('cart.cart'))

    # Calculate total from cart items
    total = 0
    cart_items_detail = []

    for product_id, quantity in cart.items():
        product = db_helper.get_product_by_id(product_id)

        if not product:
            seller_usernames = ['seller1', 'seller2']  # For now, hardcoded sellers from models
            for seller in seller_usernames:
                product = db_helper.get_seller_product_by_id(seller, product_id)
                if product:
                    break

        if product:
            item_total = product['price_inr'] * quantity
            total += item_total
            cart_items_detail.append(f"{product['Description']} x{quantity}")

    # Add buy-now item to total if present
    buy_now_detail = ""
    if buy_now_item:
        buy_now_total = buy_now_item['product']['price_inr'] * buy_now_item['quantity']
        total += buy_now_total
        buy_now_detail = f"{buy_now_item['product']['Description']} x{buy_now_item['quantity']}"

    # Clear cart and buy-now item after successful checkout
    session.pop('cart', None)
    session.pop('buy_now_item', None)
    session.modified = True

    # Mask card number for security (show only last 4 digits)
    masked_card = f"**** **** **** {card_number[-4:]}"

    # Create order summary
    if cart_items_detail and buy_now_detail:
        order_summary = "Checkout completed successfully! Items: " + ", ".join(cart_items_detail) + ", " + buy_now_detail
    elif cart_items_detail:
        order_summary = "Checkout completed successfully! Items: " + ", ".join(cart_items_detail)
    else:
        order_summary = f"Checkout completed successfully! Item: {buy_now_detail}"

    order_summary += f"<br>Ship to: {name}"
    order_summary += f"<br>Address: {address}"
    order_summary += f"<br>Payment: {masked_card}"

    flash(order_summary, 'success')
    return redirect(url_for('product.home'))

@order_bp.route('/buy_now_checkout', methods=['GET', 'POST'])
@login_required
def buy_now_checkout():
    buy_now_item = session.get('buy_now_item')
    
    # Check if there's a buy-now item to process
    if not buy_now_item:
        flash('No buy-now item found', 'error')
        return redirect(url_for('product.home'))
    
    if request.method == 'POST':
        checkout_type = request.form.get('checkout_type', 'quick')
        product = buy_now_item['product']
        quantity = buy_now_item['quantity']
        # Handle both price_inr (main products) and price (seller products)
        price = product.get('price_inr', product.get('price', 0))
        total = price * quantity
        
        if checkout_type == 'quick':
            # Process immediate buy-now purchase (no form data required)
            order_summary = f"Quick purchase completed successfully! {product['name']} x{quantity} - Total: ${total:.2f}"
            
        elif checkout_type == 'normal':
            # Process normal checkout with form data
            name = request.form.get('name', '').strip()
            address = request.form.get('address', '').strip()
            card_number = request.form.get('card_number', '').strip()
            expiry_date = request.form.get('expiry_date', '').strip()
            cvv = request.form.get('cvv', '').strip()
            
            # Validate required fields
            if not all([name, address, card_number, expiry_date, cvv]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('order.buy_now_checkout'))
            
            # Basic card number validation (demo purposes)
            if len(card_number.replace(' ', '')) < 13:
                flash('Invalid card number', 'error')
                return redirect(url_for('order.buy_now_checkout'))
            
            # Basic expiry date validation
            try:
                month, year = expiry_date.split('/')
                if int(month) < 1 or int(month) > 12:
                    raise ValueError('Invalid month')
            except:
                flash('Invalid expiry date format (MM/YY)', 'error')
                return redirect(url_for('order.buy_now_checkout'))
            
            # Basic CVV validation
            if len(cvv) < 3:
                flash('Invalid CVV', 'error')
                return redirect(url_for('order.buy_now_checkout'))
            
            # Mask card number for security (show only last 4 digits)
            masked_card = f"**** **** **** {card_number[-4:]}"
            
            order_summary = f"Checkout completed successfully! {product['name']} x{quantity} - Total: ${total:.2f}"
            order_summary += f"<br>Ship to: {name}"
            order_summary += f"<br>Address: {address}"
            order_summary += f"<br>Payment: {masked_card}"
        
        # Clear buy-now item after successful purchase
        session.pop('buy_now_item', None)
        session.modified = True
        
        # Create success message
        flash(order_summary, 'success')
        
        return redirect(url_for('product.home'))
    
    # GET request - show buy-now checkout confirmation
    product = buy_now_item['product']
    quantity = buy_now_item['quantity']
    # Handle both price_inr (main products) and price (seller products)
    price = product.get('price_inr', product.get('price', 0))
    total = price * quantity
    
    return render_template('buy_now_checkout.html', 
                         product=product, 
                         quantity=quantity, 
                         total=total)
