from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import auth_bp, inventory_bp, orders_bp, suppliers_bp, dashboard_bp, warehouse_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(warehouse_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
