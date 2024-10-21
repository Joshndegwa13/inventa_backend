# services/finance_service.py

from models import FinanceReport, Sale, Product
from database import db

def get_all_finance_reports():
    return FinanceReport.query.all()

def create_finance_report(data):
    new_report = FinanceReport(
        total_sales=data.get('total_sales', 0.0),
        expenses=data.get('expenses', 0.0),
        profits=data.get('profits', 0.0),
        report_date=data.get('report_date')
    )
    db.session.add(new_report)
    db.session.commit()
    return new_report

def get_latest_finance_report():
    # Get the latest sales data to calculate profits
    sales = Sale.query.all()
    
    total_sales = sum(sale.stock_amount * Product.query.filter_by(sku=sale.sku).first().price for sale in sales)
    total_cost = sum(sale.stock_amount * Product.query.filter_by(sku=sale.sku).first().cost for sale in sales)
    total_profits = total_sales - total_cost

    latest_report = FinanceReport.query.order_by(FinanceReport.report_date.desc()).first()
    
    if latest_report:
        latest_report.total_sales = total_sales
        latest_report.expenses = total_cost  # You can modify this based on your needs
        latest_report.profits = total_profits
        db.session.commit()
        
    return {
        "total_sales": total_sales,
        "expenses": total_cost,
        "profits": total_profits,
        "report_date": latest_report.report_date if latest_report else None,
    }
