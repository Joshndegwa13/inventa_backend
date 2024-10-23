# routes/product_routes.py
import csv
import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from typing import Dict
from services.product_service import (
    get_all_products,
    add_product,
    delete_product
)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv'}

product_bp = Blueprint('product_bp', __name__)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product_bp.route('/', methods=['GET'])
def get_products():
    products = get_all_products()
    return jsonify([product.to_dict() for product in products])

@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    new_product, errors = add_product(data)
    if errors:
        return jsonify({'errors': errors}), 400
    return jsonify(new_product.to_dict()), 201

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    success = delete_product(product_id)
    if success:
        return jsonify({'message': 'Product deleted'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


@product_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:  # type: Dict[str, str]
                try:
                    product_data = {
                        'name': row.get('name', '').strip(),
                        'sku': row.get('sku', '').strip(),
                        'price': float(row.get('price', 0) or 0),
                        'stock_amount': int(row.get('stock_amount', 0) or 0),
                        'description': row.get('description', '').strip(),  # Optional field
                        'cost': float(row.get('cost', 0) or 0)  # Default to 0 if not provided
                    }
                except (ValueError, KeyError) as e:
                    return jsonify({'error': f'Invalid data format in CSV file: {e}'}), 400

                # Use the add_product function from the service
                new_product, errors = add_product(product_data)
                if errors:
                    return jsonify({'errors': errors}), 400

        return jsonify({'message': 'CSV file successfully processed'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400