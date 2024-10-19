# services/product_service.py

from models import Product
from database import db
from utils.validators import validate_product_data

def get_all_products():
    return Product.query.all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

# services/product_service.py

def add_product(data):
    errors = validate_product_data(data)
    if errors:
        return None, errors

    new_product = Product(
        sku=data['sku'],
        name=data['name'],
        description=data['description'],
        stock_amount=data['stock_amount'],
        price=data['price'],
        cost=data.get('cost', 0)  # Default cost to 0 if not provided
    )

    db.session.add(new_product)
    db.session.commit()
    return new_product, None


def delete_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return True
    return False