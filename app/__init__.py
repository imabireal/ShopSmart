from flask import Flask, request
from config import Config
from app.extensions import init_extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)

    # Import utils inside the function to avoid circular imports
    from app.utils import utils

    # Global before_request to clean session for all routes
    @app.before_request
    def clean_session():
        """Clean session before each request to prevent serialization errors"""
        try:
            # Get the request path to determine if we're in checkout flow
            request_path = request.path
            
            # Don't clean cart/buy_now_item if we're on checkout pages
            # This prevents session clearing during active checkout
            # Important: Order matters - check exact matches first, then prefixes
            # Use path startswith for prefix matching to avoid false positives
            
            # Exact matches (must check first to avoid false positives)
            is_exact_checkout_route = request_path in ['/buy_now_checkout', '/checkout']
            
            # Prefix matches (must have proper path boundaries)
            # /buy_now/ requires following / or end of string
            is_buy_now_prefix = (
                request_path.startswith('/buy_now/') or
                request_path == '/buy_now' or
                request_path.startswith('/buy_now_checkout/')
            )
            
            is_checkout_flow = is_exact_checkout_route or is_buy_now_prefix
            
            if not is_checkout_flow:
                # Clean cart data only when not in checkout flow
                utils.clean_cart_session()
                # Clean buy-now item data only when not in checkout flow
                utils.clean_buy_now_session()
        except Exception as e:
            # If cleaning fails, reset entire session
            utils.reset_session()

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.order_routes import order_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)

    return app
