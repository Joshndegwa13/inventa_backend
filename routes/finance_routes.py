# routes/finance_routes.py

from flask import Blueprint, jsonify
from services.finance_service import get_all_finance_reports, get_latest_finance_report

finance_bp = Blueprint('finance_bp', __name__)

@finance_bp.route('/', methods=['GET'])
def get_finances():
    reports = get_all_finance_reports()
    return jsonify([report.to_dict() for report in reports])

@finance_bp.route('/latest', methods=['GET'])
def get_latest_finance():
    report = get_latest_finance_report()
    if report:
        return jsonify(report)
    else:
        return jsonify({"message": "No finance reports found"}), 404
