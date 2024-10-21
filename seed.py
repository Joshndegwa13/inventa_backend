from datetime import datetime, timedelta
from app import create_app  # Import the create_app function
from models import db, Product, Sale  # Ensure models are imported correctly

# Initialize the Flask app context
app = create_app()

with app.app_context():
    # Clear existing data
    db.session.query(Sale).delete()
    db.session.query(Product).delete()
    db.session.commit()

    # Seed Product data
    product_data = [
        {'sku': 'ABC123', 'name': 'Product A', 'description': 'Description for Product A', 'price': 150.0, 'cost': 100.0, 'stock_amount': 100},
        {'sku': 'DEF456', 'name': 'Product B', 'description': 'Description for Product B', 'price': 120.0, 'cost': 80.0, 'stock_amount': 150},
        {'sku': 'GHI789', 'name': 'Product C', 'description': 'Description for Product C', 'price': 180.0, 'cost': 140.0, 'stock_amount': 200},
        {'sku': 'JKL012', 'name': 'Product D', 'description': 'Description for Product D', 'price': 170.0, 'cost': 130.0, 'stock_amount': 80},
        {'sku': 'MNO345', 'name': 'Product E', 'description': 'Description for Product E', 'price': 200.0, 'cost': 160.0, 'stock_amount': 60},
    ]

    # Create Product instances and add them to the session
    for item in product_data:
        new_product = Product(
            sku=item['sku'],
            name=item['name'],
            description=item['description'],
            price=item['price'],
            cost=item['cost'],
            stock_amount=item['stock_amount']
        )
        db.session.add(new_product)

    db.session.commit()
    print("Products seeded successfully!")

    # Fetch products to link to sales
    products = Product.query.all()

    # Seed Sale data for the last 4 days
    for day in range(4):
        sale_date = datetime.utcnow() - timedelta(days=day)

        # Create sales data for each product, with increasing stock amount sold
        sales_data = [
            {
                "customer_name": f"Customer {day * len(products) + i + 1}", 
                "sku": product.sku, 
                "stock_amount": (i + 1) * 10  # Adjust multiplier for the number of items sold
            } 
            for i, product in enumerate(products)
        ]

        for sale_data in sales_data:
            product = Product.query.filter_by(sku=sale_data["sku"]).first()

            # Check if product exists and has enough stock
            if product and product.stock_amount >= sale_data["stock_amount"]:
                total_sales = sale_data["stock_amount"] * product.price  # Calculate total sales

                new_sale = Sale(
                    customer_name=sale_data["customer_name"],
                    stock_amount=sale_data["stock_amount"],
                    sku=product.sku,
                    product=product,
                    sale_date=sale_date
                )
                # Deduct stock_amount from product's stock
                product.stock_amount -= sale_data["stock_amount"]
                db.session.add(new_sale)

                print(f"Sale added for {sale_data['customer_name']} of {sale_data['stock_amount']} units of {product.name}. Total Sales: {total_sales:.2f}")

    db.session.commit()
    print("Sales seeded successfully!")
