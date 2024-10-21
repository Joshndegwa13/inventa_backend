from flask import Blueprint, request, jsonify
from models import Sale, Product, Invoice, db
from services.sales_service import create_sale
from sqlalchemy import func

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
    # Check if the client requests aggregated sales data by date
    if request.args.get('aggregate') == 'true':
        sales_data = db.session.query(
            func.date(Sale.sale_date).label('date'),
            func.sum(Sale.stock_amount * Product.price).label('total_sales')
        ).join(Product, Sale.sku == Product.sku)\
         .group_by(func.date(Sale.sale_date))\
         .order_by(func.date(Sale.sale_date)).all()

        # Format the aggregated data to return it as JSON
        result = [{'date': str(sale.date), 'total_sales': float(sale.total_sales)} for sale in sales_data]

        return jsonify(result)

    # Otherwise, return the individual sales records
    sales = Sale.query.all()
    return jsonify([sale.to_dict() for sale in sales])

@bp.route('/<int:id>', methods=['GET'])
def get_sale(id):
    sale = Sale.query.get_or_404(id)
    return jsonify(sale.to_dict())

