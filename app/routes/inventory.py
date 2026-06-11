from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Supplier

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/products')
@login_required
def products_list():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=20)
    return render_template('products.html', products=products)

@inventory_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            sku=request.form.get('sku'),
            category=request.form.get('category'),
            price=float(request.form.get('price', 0)),
            cost=float(request.form.get('cost', 0)),
            quantity_in_stock=int(request.form.get('quantity_in_stock', 0)),
            reorder_level=int(request.form.get('reorder_level', 10)),
            supplier_id=request.form.get('supplier_id') or None
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Prekė {product.name} sukurta sėkmingai', 'success')
        return redirect(url_for('inventory.products_list'))
    
    suppliers = Supplier.query.all()
    return render_template('product_form.html', suppliers=suppliers)

@inventory_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.sku = request.form.get('sku')
        product.category = request.form.get('category')
        product.price = float(request.form.get('price', 0))
        product.cost = float(request.form.get('cost', 0))
        product.quantity_in_stock = int(request.form.get('quantity_in_stock', 0))
        product.reorder_level = int(request.form.get('reorder_level', 10))
        product.supplier_id = request.form.get('supplier_id') or None
        db.session.commit()
        flash(f'Prekė {product.name} atnaujinta sėkmingai', 'success')
        return redirect(url_for('inventory.products_list'))
    
    suppliers = Supplier.query.all()
    return render_template('product_form.html', product=product, suppliers=suppliers)

@inventory_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Prekė {product.name} ištrinta sėkmingai', 'success')
    return redirect(url_for('inventory.products_list'))

@inventory_bp.route('/api/products')
@login_required
def api_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'price': p.price,
        'quantity_in_stock': p.quantity_in_stock,
        'is_low_stock': p.is_low_stock()
    } for p in products])
