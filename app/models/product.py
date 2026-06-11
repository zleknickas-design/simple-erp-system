from app import db
from datetime import datetime
import os

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float)  # Cost price for COGS calculation
    quantity_in_stock = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)  # Minimum stock level
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    is_active = db.Column(db.Boolean, default=True)
    image_filename = db.Column(db.String(255))  # Store image filename
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = db.relationship('Supplier', backref='products')
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level
    
    def get_image_url(self):
        """Get the URL path for the product image"""
        if self.image_filename:
            return f'/uploads/products/{self.image_filename}'
        return '/static/images/no-image.png'
    
    def __repr__(self):
        return f'<Product {self.name}>'
