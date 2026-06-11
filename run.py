import os
from app import create_app, db
from app.models import User, Product, Order, Supplier, FinancialTransaction

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Order': Order,
        'Supplier': Supplier,
        'FinancialTransaction': FinancialTransaction
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
