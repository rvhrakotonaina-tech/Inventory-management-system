from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev')

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'inventory_db')

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Products routes
@app.route('/products')
def products():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.*, s.name as supplier_name 
        FROM Products p 
        LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
    """)
    products = cur.fetchall()
    cur.close()
    return render_template('products.html', products=products)

# Suppliers routes
@app.route('/suppliers')
def suppliers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return render_template('suppliers.html', suppliers=suppliers)

# Sales routes
@app.route('/sales')
def sales():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT s.sale_id, p.name as product_name, s.quantity_sold, s.sale_date, 
               (s.quantity_sold * p.price) as total_amount
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        ORDER BY s.sale_date DESC
    """)
    sales = cur.fetchall()
    
    # Get products for the sales form
    cur.execute("SELECT product_id, name FROM Products")
    products = cur.fetchall()
    cur.close()
    
    return render_template('sales.html', sales=sales, products=products)

# API Endpoints
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO Products (name, price, quantity, date_added, supplier_id)
            VALUES (%s, %s, %s, %s, %s)
        ""
