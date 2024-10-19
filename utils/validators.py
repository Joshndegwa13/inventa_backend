# utils/validators.py

# utils/validators.py

def validate_product_data(data):
    errors = []

    # Convert price and quantity to the appropriate types
    try:
        data['price'] = float(data['price'])  # Convert price to a float
    except ValueError:
        errors.append("Price must be a valid number.")

    try:
        data['stock_amount'] = int(data['stock_amount'])  # Convert stock_amount to an integer
    except ValueError:
        errors.append("Stock Amount must be a valid integer.")

    # Perform validation
    if 'name' not in data or not data['name']:
        errors.append("Name is required.")
    if 'price' in data and data['price'] < 0:
        errors.append("Price must be a positive value.")
    if 'stock_amount' in data and data['stock_amount'] < 0:
        errors.append("Stock Amount cannot be negative.")

    return errors


def validate_sale_data(data):
    errors = []

    # Convert amount to the appropriate type
    try:
        data['stock_amount'] = float(data['stock_amount'])  # Convert stock_amount to a float
    except ValueError:
        errors.append("Stock amount must be a valid number.")

    if 'customer_name' not in data or not data['customer_name']:
        errors.append('Customer name is required.')
    if 'stock_amount' in data and data['stock_amount'] <= 0:
        errors.append('Stock amount must be a positive number.')
    if 'sku' not in data or not isinstance(data['sku'], str):
        errors.append('SKU is required and must be a string.')

    return errors