from database import db
from utils.helpers import format_datetime
from datetime import datetime
from sqlalchemy.orm import relationship



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    stock_amount = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)  # Cost field added
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    sales = relationship('Sale', back_populates='product')


    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'stock_amount': self.stock_amount,
            'price': self.price,
            'cost': self.cost,
            'created_at': format_datetime(self.created_at),
            'updated_at': format_datetime(self.updated_at),
        }

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), db.ForeignKey('product.sku'), nullable=False)
    stock_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, paid, canceled
    issued_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'stock_amount': self.stock_amount,
            'status': self.status,
            'issued_at': format_datetime(self.issued_at),
        }

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    delivery_status = db.Column(db.String(50), default='pending')  # pending, shipped, delivered
    address = db.Column(db.String(200), nullable=False)
    delivery_date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'delivery_status': self.delivery_status,
            'address': self.address,
            'delivery_date': format_datetime(self.delivery_date) if self.delivery_date else None,
        }

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    stock_amount = db.Column(db.Float, nullable=False)
    sku = db.Column(db.String(50), db.ForeignKey('product.sku'), nullable=False)
    product = db.relationship('Product', backref='sales', lazy=True)
    delivery_status = db.Column(db.String(50), default='pending')
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=True)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)

    product = relationship('Product', back_populates='sales')


    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'stock_amount': self.stock_amount,
            'sale_date': self.sale_date.isoformat(),
            'sku': self.sku,
            'product_name': self.product.name,
            'delivery_status': self.delivery_status,
            'invoice_id': self.invoice_id
        }

class FinanceReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_sales = db.Column(db.Float, default=0.0)
    expenses = db.Column(db.Float, default=0.0)
    profits = db.Column(db.Float, default=0.0)
    report_date = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'total_sales': self.total_sales,
            'expenses': self.expenses,
            'profits': self.profits,
            'report_date': format_datetime(self.report_date),
        }