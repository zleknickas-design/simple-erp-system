from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, Product
from datetime import datetime
import uuid

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
@login_required
def orders_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    
    query = Order.query
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('orders.html', orders=orders, current_status=status)

@orders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_order():
    if request.method == 'POST':
        order = Order(
            order_number=f"UŽS-{uuid.uuid4().hex[:8].upper()}",
            customer_name=request.form.get('customer_name'),
            customer_email=request.form.get('customer_email'),
            customer_phone=request.form.get('customer_phone'),
            delivery_address=request.form.get('delivery_address'),
            created_by=current_user.id,
            notes=request.form.get('notes')
        )
        db.session.add(order)
        db.session.flush()
        
        # Add order items
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        
        for prod_id, qty in zip(product_ids, quantities):
            if prod_id and qty:
                product = Product.query.get(prod_id)
                if product:
                    item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=int(qty),
                        unit_price=product.price
                    )
                    item.calculate_subtotal()
                    db.session.add(item)
        
        order.calculate_total()
        db.session.commit()
        flash(f'Užsakymas {order.order_number} sukurtas sėkmingai', 'success')
        return redirect(url_for('orders.view_order', id=order.id))
    
    products = Product.query.filter_by(is_active=True).all()
    return render_template('order_form.html', products=products)

@orders_bp.route('/<int:id>')
@login_required
def view_order(id):
    order = Order.query.get_or_404(id)
    return render_template('order_detail.html', order=order)

@orders_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    
    if request.method == 'POST':
        order.customer_name = request.form.get('customer_name')
        order.customer_email = request.form.get('customer_email')
        order.customer_phone = request.form.get('customer_phone')
        order.delivery_address = request.form.get('delivery_address')
        order.notes = request.form.get('notes')
        order.status = request.form.get('status')
        order.paid_amount = float(request.form.get('paid_amount', 0))
        db.session.commit()
        flash('Užsakymas atnaujintas sėkmingai', 'success')
        return redirect(url_for('orders.view_order', id=order.id))
    
    return render_template('order_form.html', order=order)

@orders_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash('Užsakymas ištrintas sėkmingai', 'success')
    return redirect(url_for('orders.orders_list'))

@orders_bp.route('/api/orders')
@login_required
def api_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'order_number': o.order_number,
        'customer_name': o.customer_name,
        'status': o.status,
        'total_amount': o.total_amount,
        'created_at': o.created_at.isoformat()
    } for o in orders])
