# Simple ERP System

A lightweight Enterprise Resource Planning (ERP) system built with Python and Flask, featuring inventory management, order processing, and basic financial tracking.

## Features

- **Inventory Management**: Track products, stock levels, and warehouse locations
- **Order Management**: Create, process, and track customer orders
- **Supplier Management**: Manage suppliers and purchase orders
- **Financial Tracking**: Basic income and expense tracking
- **Dashboard**: Overview of key business metrics
- **User Authentication**: Secure login system

## Project Structure

```
simple-erp-system/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── supplier.py
│   │   └── financial.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── inventory.py
│   │   ├── orders.py
│   │   ├── suppliers.py
│   │   └── dashboard.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── products.html
│   │   ├── orders.html
│   │   └── suppliers.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── migrations/
├── requirements.txt
├── config.py
├── run.py
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/zleknickas-design/simple-erp-system.git
cd simple-erp-system
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

5. Run the application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Default Login

- **Username**: admin
- **Password**: admin123

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/register` - User registration

### Inventory
- `GET /api/products` - List all products
- `POST /api/products` - Create new product
- `GET /api/products/<id>` - Get product details
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Orders
- `GET /api/orders` - List all orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<id>` - Get order details
- `PUT /api/orders/<id>` - Update order status

### Suppliers
- `GET /api/suppliers` - List all suppliers
- `POST /api/suppliers` - Create new supplier
- `GET /api/suppliers/<id>` - Get supplier details

### Dashboard
- `GET /api/dashboard/summary` - Get business summary

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Authentication**: Flask-Login, bcrypt
- **ORM**: SQLAlchemy

## License

MIT License
