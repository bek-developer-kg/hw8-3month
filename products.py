PRODUCTS = {
    "product_1": {"name": "Ноутбук HP", "desc": "Ноутбук HP Victus 15 Gaming 15.6 144HZ AMD Ryzen 5 8645HS Nvidia GeForce RTX 4050 6gb", "price": "69900сом."},
    "product_2": {"name": "Ноутбук Asus", "desc": "Ноутбук ASUS TUF Gaming F15 15.6 144HZ Intel Core i5-10300H GeForce GTX 1650", "price": "64000сом."},
}

user_orders = {}

def get_products():
    return PRODUCTS

def get_product_info(user_id, product_key):
    product = PRODUCTS.get(product_key)
    user_orders[user_id] = product
    return product

def confirm_order(user_id):
    order = user_orders.get(user_id)
    if order:
        user_orders.pop(user_id, None)
        return f"Ваш заказ принят: {order['name']}\nОписание: {order['desc']}\nЦена: {order['price']}"
    return "Сначала выберите товар."

def cancel_order(user_id):
    user_orders.pop(user_id, None)
