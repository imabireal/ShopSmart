from flask import session
import logging

# Set up logging
logger = logging.getLogger('flask-ecommerce')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def clean_cart_session():
    """Clean and validate cart data in session to prevent serialization errors"""
    try:
        cart = session.get('cart', {})
        
        if not isinstance(cart, dict):
            session['cart'] = {}
            session.modified = True
            return {}
        
        cleaned_cart = {}
        for k, v in cart.items():
            try:
                if k is None or v is None:
                    continue
                
                key = str(k) if isinstance(k, (int, str)) else None
                value = int(v) if isinstance(v, (int, str)) else None
                
                if key and value and value > 0:
                    cleaned_cart[key] = value
            except (ValueError, TypeError):
                continue
        
        sorted_cart = dict(sorted(cleaned_cart.items()))
        
        if sorted_cart != cart:
            session['cart'] = sorted_cart
            session.modified = True
        
        return sorted_cart
        
    except Exception as e:
        logger.error(f"Cart cleaning error: {e}")
        session['cart'] = {}
        session.modified = True
        return {}


def clean_buy_now_session():
    """Clean and validate buy-now item in session"""
    try:
        buy_now_item = session.get('buy_now_item')
        if not buy_now_item:
            return None
        
        if not isinstance(buy_now_item, dict):
            logger.warning("buy_now_item is not a dict, removing")
            session.pop('buy_now_item', None)
            session.modified = True
            return None
        
        if 'product' not in buy_now_item or 'quantity' not in buy_now_item:
            logger.warning("buy_now_item missing required keys, removing")
            session.pop('buy_now_item', None)
            session.modified = True
            return None
        
        product = buy_now_item['product']
        quantity = buy_now_item['quantity']
        
        if not isinstance(product, dict):
            logger.warning("buy_now_item.product is not a dict, removing")
            session.pop('buy_now_item', None)
            session.modified = True
            return None
        
        if not isinstance(quantity, int) or quantity <= 0:
            logger.warning("buy_now_item.quantity is invalid, removing")
            session.pop('buy_now_item', None)
            session.modified = True
            return None
        
        return buy_now_item
    except Exception as e:
        logger.error(f"Buy-now cleaning error: {e}")
        session.pop('buy_now_item', None)
        session.modified = True
        return None


def reset_session():
    """Reset all session data"""
    session.clear()
    session.modified = True


def validate_checkout_data(name, address, card_number, expiry_date, cvv):
    """Validate checkout form data"""
    errors = []
    
    if not name or not name.strip():
        errors.append('Name is required')
    
    if not address or not address.strip():
        errors.append('Address is required')
    
    if not card_number or len(card_number.replace(' ', '')) < 13:
        errors.append('Invalid card number')
    
    if not expiry_date:
        errors.append('Expiry date is required')
    else:
        try:
            month, year = expiry_date.split('/')
            if int(month) < 1 or int(month) > 12:
                errors.append('Invalid expiry month')
        except:
            errors.append('Invalid expiry date format (MM/YY)')
    
    if not cvv or len(cvv) < 3:
        errors.append('Invalid CVV')
    
    return errors


def mask_card_number(card_number):
    """Mask card number for security, showing only last 4 digits"""
    if not card_number:
        return ''
    card_number = card_number.replace(' ', '')
    if len(card_number) < 4:
        return card_number
    return f"**** **** **** {card_number[-4:]}"
