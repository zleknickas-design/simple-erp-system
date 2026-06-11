from app import db
from datetime import datetime

class FinancialTransaction(db.Model):
    __tablename__ = 'financial_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)  # income, expense
    category = db.Column(db.String(100))  # sales, supplies, salary, etc.
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    reference_type = db.Column(db.String(50))  # order, purchase_order, etc.
    reference_id = db.Column(db.Integer)
    payment_method = db.Column(db.String(50))  # cash, check, bank_transfer, credit_card
    transaction_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FinancialTransaction {self.category} - {self.amount}>'
