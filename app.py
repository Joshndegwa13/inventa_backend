import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from database import db
from routes.product_routes import product_bp
from routes.finance_routes import finance_bp
from routes.delivery_routes import delivery_bp
from routes.invoice_routes import invoice_bp
from routes.sales_routes import sales_bp


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(finance_bp, url_prefix='/api/finances')
    app.register_blueprint(delivery_bp, url_prefix='/api/delivery')
    app.register_blueprint(invoice_bp, url_prefix='/api/invoices')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify(message="Welcome to the Inventory Management API! Refer to /api for more information.")

    return app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5555))  # Use PORT environment variable or fallback to 5000
    app = create_app()  # Call create_app to initialize the app
    app.run(host='0.0.0.0', port=port)
