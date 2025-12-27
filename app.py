from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user database (in a real app, use a proper database)
users = {}

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

def clean_cart_session():
    """Clean and validate cart data in session to prevent serialization errors"""
    try:
        cart = session.get('cart', {})
        
        # If cart doesn't exist or is empty, initialize it
        if not cart:
            session['cart'] = {}
            session.modified = True
            return {}
        
        # If not a dict, reset to empty
        if not isinstance(cart, dict):
            session['cart'] = {}
            session.modified = True
            return {}
        
        # Clean up cart data - ensure all keys and values are strictly integers
        cleaned_cart = {}
        for k, v in cart.items():
            try:
                # Skip if key or value is None
                if k is None or v is None:
                    continue
                    
                # Force conversion to int for both keys and values
                key = int(k) if isinstance(k, (int, str)) else None
                value = int(v) if isinstance(v, (int, str)) else None
                
                if key is not None and value is not None and key > 0 and value > 0:
                    cleaned_cart[key] = value
            except (ValueError, TypeError):
                continue  # Skip invalid entries
        
        # Sort keys to ensure consistent ordering (prevents comparison issues)
        sorted_cart = {k: cleaned_cart[k] for k in sorted(cleaned_cart.keys())}
        
        # Only update session if we made changes
        if sorted_cart != cart:
            session['cart'] = sorted_cart
            session.modified = True
        
        return sorted_cart
        
    except Exception as e:
        # Only reset cart if there's a serious error, not just data type issues
        print(f"Cart cleaning error: {e}")
        # Reset cart on any error to prevent serialization issues
        session['cart'] = {}
        session.modified = True
        return {}

def clean_buy_now_session():
    """Clean and validate buy-now item data in session to prevent serialization errors"""
    try:
        buy_now_item = session.get('buy_now_item')
        
        if not buy_now_item:
            return None
        
        # Reset if not a dict
        if not isinstance(buy_now_item, dict):
            session.pop('buy_now_item', None)
            session.modified = True
            return None
        
        # Validate required fields
        required_fields = ['product_id', 'quantity', 'product']
        if not all(field in buy_now_item for field in required_fields):
            session.pop('buy_now_item', None)
            session.modified = True
            return None
        
        # Validate product_id and quantity are integers
        try:
            buy_now_item['product_id'] = int(buy_now_item['product_id'])
            buy_now_item['quantity'] = int(buy_now_item['quantity'])
            
            if buy_now_item['product_id'] <= 0 or buy_now_item['quantity'] <= 0:
                session.pop('buy_now_item', None)
                session.modified = True
                return None
                
        except (ValueError, TypeError):
            session.pop('buy_now_item', None)
            session.modified = True
            return None
        
        # Only update session if we made changes
        session['buy_now_item'] = buy_now_item
        session.modified = True
        return buy_now_item
        
    except Exception as e:
        # Only reset buy-now item if there's a serious error
        print(f"Buy-now session cleaning error: {e}")
        return None

def reset_session():
    """Completely reset session to prevent corruption"""
    session.clear()
    session['cart'] = {}
    session.modified = True

@app.before_request
def before_request():
    """Clean session before each request to prevent serialization errors"""
    try:
        # Clean cart data
        clean_cart_session()
        # Clean buy-now item data
        clean_buy_now_session()
    except Exception as e:
        # If cleaning fails, reset entire session
        reset_session()

# Mock products
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10.99},
    {'id': 2, 'name': 'Product 2', 'price': 15.99},
    {'id': 3, 'name': 'Product 3', 'price': 20.99},
]

@app.route('/')
def home():
    # Clean and validate cart from session
    cart = clean_cart_session()
    cart_count = sum(cart.values()) if cart else 0
    return render_template('home.html', products=products, cart=cart, cart_count=cart_count, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users.values() if u.username == username and u.password == password), None)
        if user:
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in [u.username for u in users.values()]:
            flash('Username already exists')
        else:
            user_id = len(users) + 1
            users[user_id] = User(user_id, username, password)
            flash('Account created successfully. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Cart management routes
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({
            'success': False, 
            'message': 'Please log in to add items to cart',
            'redirect': url_for('login')
        })
    
    # Check if product exists
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    # Get and clean cart from session
    cart = clean_cart_session()
    
    # Convert product_id to int and add or update item in cart
    product_id = int(product_id)
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
        'message': f'{product["name"]} added to cart',
        'cart_count': cart_count
    })

@app.route('/cart')
@login_required
def cart():
    # Clean and validate cart from session
    cart = clean_cart_session()
    
    cart_items = []
    cart_total = 0
    
    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
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

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity', 0))
    
    cart = session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity
    
    # Ensure all values are integers
    cart = {k: int(v) for k, v in cart.items()}
    
    session['cart'] = cart
    session.modified = True
    
    cart_count = sum(cart.values())
    
    return jsonify({'success': True, 'cart_count': cart_count})

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(product_id, None)
    session['cart'] = cart
    
    cart_count = sum(cart.values())
    
    return jsonify({'success': True, 'cart_count': cart_count})

@app.route('/buy_now/<int:product_id>')
@login_required
def buy_now(product_id):
    # Check if product exists
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('home'))
    
    # Store buy-now item in separate session variable
    session['buy_now_item'] = {
        'product_id': product_id,
        'quantity': 1,
        'product': product
    }
    session.modified = True
    
    # Redirect to immediate buy-now checkout
    return redirect(url_for('buy_now_checkout'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    buy_now_item = session.get('buy_now_item')

    # Check if there's something to checkout
    if not cart and not buy_now_item:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))

    # Get checkout data
    name = request.form.get('name', '').strip()
    address = request.form.get('address', '').strip()
    card_number = request.form.get('card_number', '').strip()
    expiry_date = request.form.get('expiry_date', '').strip()
    cvv = request.form.get('cvv', '').strip()

    # Validate required fields
    if not all([name, address, card_number, expiry_date, cvv]):
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('cart'))

    # Basic card number validation (demo purposes)
    if len(card_number.replace(' ', '')) < 13:
        flash('Invalid card number', 'error')
        return redirect(url_for('cart'))

    # Basic expiry date validation
    try:
        month, year = expiry_date.split('/')
        if int(month) < 1 or int(month) > 12:
            raise ValueError('Invalid month')
    except:
        flash('Invalid expiry date format (MM/YY)', 'error')
        return redirect(url_for('cart'))

    # Basic CVV validation
    if len(cvv) < 3:
        flash('Invalid CVV', 'error')
        return redirect(url_for('cart'))

    # Calculate total from cart items
    total = 0
    cart_items_detail = []

    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            total += item_total
            cart_items_detail.append(f"{product['name']} x{quantity}")

    # Add buy-now item to total if present
    buy_now_detail = ""
    if buy_now_item:
        buy_now_total = buy_now_item['product']['price'] * buy_now_item['quantity']
        total += buy_now_total
        buy_now_detail = f"{buy_now_item['product']['name']} x{buy_now_item['quantity']}"

    # Clear buy-now item after successful checkout (but keep cart items)
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
    return redirect(url_for('home'))

@app.route('/buy_now_checkout', methods=['GET', 'POST'])
@login_required
def buy_now_checkout():
    buy_now_item = session.get('buy_now_item')
    
    # Check if there's a buy-now item to process
    if not buy_now_item:
        flash('No buy-now item found', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        checkout_type = request.form.get('checkout_type', 'quick')
        product = buy_now_item['product']
        quantity = buy_now_item['quantity']
        total = product['price'] * quantity
        
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
                return redirect(url_for('buy_now_checkout'))
            
            # Basic card number validation (demo purposes)
            if len(card_number.replace(' ', '')) < 13:
                flash('Invalid card number', 'error')
                return redirect(url_for('buy_now_checkout'))
            
            # Basic expiry date validation
            try:
                month, year = expiry_date.split('/')
                if int(month) < 1 or int(month) > 12:
                    raise ValueError('Invalid month')
            except:
                flash('Invalid expiry date format (MM/YY)', 'error')
                return redirect(url_for('buy_now_checkout'))
            
            # Basic CVV validation
            if len(cvv) < 3:
                flash('Invalid CVV', 'error')
                return redirect(url_for('buy_now_checkout'))
            
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
        
        return redirect(url_for('home'))
    
    # GET request - show buy-now checkout confirmation
    product = buy_now_item['product']
    quantity = buy_now_item['quantity']
    total = product['price'] * quantity
    
    return render_template('buy_now_checkout.html', 
                         product=product, 
                         quantity=quantity, 
                         total=total)

if __name__ == '__main__':
    app.run(debug=True)
