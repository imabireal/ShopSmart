from flask import Flask
from config import Config
from app.extensions import init_extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)

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
