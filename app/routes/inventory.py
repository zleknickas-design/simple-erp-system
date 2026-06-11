from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Supplier
from werkzeug.utils import secure_filename
import os
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_FOLDER = 'app/static/uploads/products'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_product_image(file):
    """Save uploaded image and return filename"""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        flash('Tik PNG, JPG, JPEG, GIF ir WebP failai leidžiami', 'error')
        return None
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    if file_length > MAX_FILE_SIZE:
        flash('Nuotrauka per didelė. Maksimalus dydis: 5MB', 'error')
        return None
    
    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"product_{timestamp}_{secure_filename(file.filename.rsplit('.', 1)[0])}.{ext}"
    
    # Save file
    file.seek(0)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return filename

def delete_product_image(filename):
    """Delete product image file"""
    if filename:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

@inventory_bp.route('/products')
@login_required
def products_list():
    page = request.args.get('page', 1, type=int)
    view = request.args.get('view', 'table')  # 'table' or 'grid'
    products = Product.query.paginate(page=page, per_page=20)
    return render_template('products.html', products=products, view=view)

@inventory_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        image_filename = None
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                image_filename = save_product_image(file)
                if not image_filename:
                    suppliers = Supplier.query.all()
                    return render_template('product_form.html', suppliers=suppliers)
        
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            sku=request.form.get('sku'),
            category=request.form.get('category'),
            price=float(request.form.get('price', 0)),
            cost=float(request.form.get('cost', 0)),
            quantity_in_stock=int(request.form.get('quantity_in_stock', 0)),
            reorder_level=int(request.form.get('reorder_level', 10)),
            supplier_id=request.form.get('supplier_id') or None,
            image_filename=image_filename
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
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                # Delete old image
                delete_product_image(product.image_filename)
                # Save new image
                image_filename = save_product_image(file)
                if image_filename:
                    product.image_filename = image_filename
        
        # Handle image deletion
        if request.form.get('delete_image') == 'on':
            delete_product_image(product.image_filename)
            product.image_filename = None
        
        db.session.commit()
        flash(f'Prekė {product.name} atnaujinta sėkmingai', 'success')
        return redirect(url_for('inventory.products_list'))
    
    suppliers = Supplier.query.all()
    return render_template('product_form.html', product=product, suppliers=suppliers)

@inventory_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    # Delete image file
    delete_product_image(product.image_filename)
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
        'is_low_stock': p.is_low_stock(),
        'image_url': p.get_image_url()
    } for p in products])
