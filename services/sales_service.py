from models import Sale, Product, Invoice, FinanceReport, db
from utils.validators import validate_sale_data

def create_sale(data):
    errors = validate_sale_data(data)
    if errors:
        return None, errors

    # Fetch product by SKU, or raise 404 error if not found
    product = Product.query.filter_by(sku=data['sku']).first_or_404()

    # Check if the product has enough stock
    if product.stock_amount < data['stock_amount']:
        return None, ['Insufficient stock available.']

    # Create a new sale
    new_sale = Sale(
        customer_name=data['customer_name'],
        stock_amount=data['stock_amount'],
        product=product,
        sku=product.sku
    )

    # Reduce the product stock amount
    product.stock_amount -= data['stock_amount']

    # Create an invoice for the sale
    new_invoice = Invoice(
        sku=product.sku,
        stock_amount=new_sale.stock_amount,
        status='pending'
    )
    db.session.add(new_sale)
    db.session.add(new_invoice)
    new_sale.invoice_id = new_invoice.id

    # Update finance report
    finance_report = FinanceReport.query.first()
    if not finance_report:
        finance_report = FinanceReport(total_sales=0.0, expenses=0.0, profits=0.0)
        db.session.add(finance_report)

    # Make sure total_sales is initialized
    if finance_report.total_sales is None:
        finance_report.total_sales = 0.0
    if finance_report.profits is None:
        finance_report.profits = 0.0

    # Update finance report with the new sale information
    finance_report.total_sales += product.price * new_sale.stock_amount
    finance_report.profits += (product.price - product.cost) * new_sale.stock_amount

    # Commit changes to the database
    db.session.commit()

    return new_sale, None
