# Mock products data
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10.99},
    {'id': 2, 'name': 'Product 2', 'price': 15.99},
    {'id': 3, 'name': 'Product 3', 'price': 20.99},
]

# Mock admins (username: password)
admins = {
    'admin': 'admin123',
    'superadmin': 'super123'
}

# Mock sellers (username: password, can manage their own products)
sellers = {
    'seller1': 'seller123',
    'seller2': 'seller456'
}

# Seller products (seller_username -> list of products)
seller_products = {
    'seller1': [
        {'id': 101, 'name': 'Seller 1 Product A', 'price': 25.99},
        {'id': 102, 'name': 'Seller 1 Product B', 'price': 30.99}
    ],
    'seller2': [
        {'id': 201, 'name': 'Seller 2 Product A', 'price': 45.99}
    ]
}

# Next product ID counters
next_product_id = 300
next_seller_product_id = 500
