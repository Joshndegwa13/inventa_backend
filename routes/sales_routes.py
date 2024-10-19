from flask import Blueprint, request, jsonify
from models import Sale, Product, Invoice, db
from services.sales_service import create_sale

bp = Blueprint('sales_routes', __name__)

@bp.route('/', methods=['POST'])
def record_sale():
    data = request.json
    new_sale, errors = create_sale(data)
    if errors:
        return jsonify({'errors': errors}), 400
    return jsonify(new_sale.to_dict()), 201

@bp.route('/', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    return jsonify([sale.to_dict() for sale in sales])

@bp.route('/<int:id>', methods=['GET'])
def get_sale(id):
    sale = Sale.query.get_or_404(id)
    return jsonify(sale.to_dict())