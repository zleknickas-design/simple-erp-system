from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Order, Product, Supplier, FinancialTransaction
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Get summary data
    total_products = Product.query.count()
    total_suppliers = Supplier.query.count()
    total_orders = Order.query.count()
    low_stock_products = Product.query.filter(Product.quantity_in_stock <= Product.reorder_level).count()
    
    # Revenue this month
    current_month_start = datetime.utcnow().replace(day=1)
    monthly_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.created_at >= current_month_start,
        Order.status == 'delivered'
    ).scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Order status summary
    pending_orders = Order.query.filter_by(status='pending').count()
    confirmed_orders = Order.query.filter_by(status='confirmed').count()
    shipped_orders = Order.query.filter_by(status='shipped').count()
    
    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_orders': total_orders,
        'low_stock_products': low_stock_products,
        'monthly_revenue': monthly_revenue,
        'recent_orders': recent_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'shipped_orders': shipped_orders
    }
    
    return render_template('dashboard.html', **context)

@dashboard_bp.route('/api/summary')
@login_required
def api_summary():
    total_products = Product.query.count()
    total_suppliers = Supplier.query.count()
    total_orders = Order.query.count()
    low_stock_products = Product.query.filter(Product.quantity_in_stock <= Product.reorder_level).count()
    
    return jsonify({
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_orders': total_orders,
        'low_stock_products': low_stock_products
    })
