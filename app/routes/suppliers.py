from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models import Supplier

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

@suppliers_bp.route('/')
@login_required
def suppliers_list():
    page = request.args.get('page', 1, type=int)
    suppliers = Supplier.query.paginate(page=page, per_page=20)
    return render_template('suppliers.html', suppliers=suppliers)

@suppliers_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_supplier():
    if request.method == 'POST':
        supplier = Supplier(
            name=request.form.get('name'),
            contact_person=request.form.get('contact_person'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            country=request.form.get('country'),
            payment_terms=request.form.get('payment_terms'),
            tax_id=request.form.get('tax_id')
        )
        db.session.add(supplier)
        db.session.commit()
        flash(f'Supplier {supplier.name} created successfully', 'success')
        return redirect(url_for('suppliers.suppliers_list'))
    
    return render_template('supplier_form.html')

@suppliers_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    
    if request.method == 'POST':
        supplier.name = request.form.get('name')
        supplier.contact_person = request.form.get('contact_person')
        supplier.email = request.form.get('email')
        supplier.phone = request.form.get('phone')
        supplier.address = request.form.get('address')
        supplier.city = request.form.get('city')
        supplier.country = request.form.get('country')
        supplier.payment_terms = request.form.get('payment_terms')
        supplier.tax_id = request.form.get('tax_id')
        db.session.commit()
        flash(f'Supplier {supplier.name} updated successfully', 'success')
        return redirect(url_for('suppliers.suppliers_list'))
    
    return render_template('supplier_form.html', supplier=supplier)

@suppliers_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash(f'Supplier {supplier.name} deleted successfully', 'success')
    return redirect(url_for('suppliers.suppliers_list'))

@suppliers_bp.route('/api/suppliers')
@login_required
def api_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'email': s.email,
        'phone': s.phone,
        'city': s.city
    } for s in suppliers])
