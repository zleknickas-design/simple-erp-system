from app.routes.auth import auth_bp
from app.routes.inventory import inventory_bp
from app.routes.orders import orders_bp
from app.routes.suppliers import suppliers_bp
from app.routes.dashboard import dashboard_bp

__all__ = ['auth_bp', 'inventory_bp', 'orders_bp', 'suppliers_bp', 'dashboard_bp']
