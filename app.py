from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure the app
    app.secret_key = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/inventory_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)

    # Import models here to avoid circular imports
    from models import Product, Supplier, Sale

    # Define routes
    @app.route('/')
    def index():
        return render_template('index.html')

    # Products routes
    @app.route('/products')
    def products():
        products = Product.query.all()
        return render_template('products.html', products=products)

    # Suppliers routes
    @app.route('/suppliers')
    def suppliers():
        suppliers = Supplier.query.all()
        return render_template('suppliers.html', suppliers=suppliers)

    # Sales routes
    @app.route('/sales')
    def sales():
        # Get all sales with product information
        sales = db.session.query(
            Sale, Product
        ).join(
            Product, Sale.product_id == Product.product_id
        ).order_by(
            Sale.sale_date.desc()
        ).all()
        
        # Format the sales data for the template
        sales_data = [{
            'sale_id': sale.sale_id,
            'product_name': product.name,
            'quantity_sold': sale.quantity_sold,
            'sale_date': sale.sale_date,
            'total_amount': float(sale.quantity_sold * product.price)
        } for sale, product in sales]
        
        # Get products for the sales form
        products = Product.query.all()
        
        return render_template('sales.html', sales=sales_data, products=products)

    # API Endpoints
    @app.route('/api/products', methods=['POST'])
    def add_product():
        data = request.get_json()
        try:
            new_product = Product(
                name=data['name'],
                price=float(data['price']),
                quantity=int(data['quantity']),
                date_added=datetime.now().date(),
                supplier_id=data.get('supplier_id')
            )
            db.session.add(new_product)
            db.session.commit()
            return jsonify({'message': 'Product added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    @app.route('/api/sales', methods=['POST'])
    def add_sale():
        data = request.get_json()
        try:
            # Start transaction
            db.session.begin()
            
            # Get the product
            product = Product.query.get(data['product_id'])
            if not product:
                return jsonify({'error': 'Product not found'}), 404
                
            # Check if enough quantity is available
            if product.quantity < int(data['quantity_sold']):
                return jsonify({'error': 'Not enough stock available'}), 400
            
            # Create new sale
            new_sale = Sale(
                product_id=data['product_id'],
                quantity_sold=int(data['quantity_sold']),
                sale_date=datetime.utcnow()
            )
            
            # Update product quantity
            product.quantity -= int(data['quantity_sold'])
            
            # Save changes
            db.session.add(new_sale)
            db.session.commit()
            
            return jsonify({'message': 'Sale recorded successfully'}), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    return app

# Define models
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    products = db.relationship('Product', backref='supplier', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.Date, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=True)
    sales = db.relationship('Sale', backref='product', lazy=True)

class Sale(db.Model):
    __tablename__ = 'sales'
    sale_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

# Products routes
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# Suppliers routes
@app.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

# Sales routes
@app.route('/sales')
def sales():
    # Get all sales with product information
    sales = db.session.query(
        Sale, Product
    ).join(
        Product, Sale.product_id == Product.product_id
    ).order_by(
        Sale.sale_date.desc()
    ).all()
    
    # Format the sales data for the template
    sales_data = [{
        'sale_id': sale.sale_id,
        'product_name': product.name,
        'quantity_sold': sale.quantity_sold,
        'sale_date': sale.sale_date,
        'total_amount': float(sale.quantity_sold * product.price)
    } for sale, product in sales]
    
    # Get products for the sales form
    products = Product.query.all()
    
    return render_template('sales.html', sales=sales_data, products=products)

# API Endpoints
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    try:
        new_product = Product(
            name=data['name'],
            price=float(data['price']),
            quantity=int(data['quantity']),
            date_added=datetime.now().date(),
            supplier_id=data.get('supplier_id')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/sales', methods=['POST'])
def add_sale():
    data = request.get_json()
    try:
        # Start transaction
        db.session.begin()
        
        # Get the product
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
            
        # Check if enough quantity is available
        if product.quantity < int(data['quantity_sold']):
            return jsonify({'error': 'Not enough stock available'}), 400
        
        # Create new sale
        new_sale = Sale(
            product_id=data['product_id'],
            quantity_sold=int(data['quantity_sold']),
            sale_date=datetime.utcnow()
        )
        
        # Update product quantity
        product.quantity -= int(data['quantity_sold'])
        
        # Save changes
        db.session.add(new_sale)
        db.session.commit()
        
        return jsonify({'message': 'Sale recorded successfully'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
