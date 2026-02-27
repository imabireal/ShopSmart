# ShopSmart Database Helper Documentation

## Overview

The ShopSmart database helper provides a high-level interface for interacting with the MongoDB database. It abstracts away the complexity of direct database operations and provides easy-to-use functions for managing users, products, orders, and sessions.

## Features

### User Management
- Create, find, and update user accounts
- Admin/Seller account management
- User authentication and password verification

### Product Management
- Main product catalog operations
- Seller-specific product management
- Product search and filtering

### Order Management
- Order creation and retrieval
- Order item management
- Cart operations integration

### Session Management
- Session data validation and cleaning
- Cart data persistence

### Data Validation
- Input validation for all operations
- Error handling and exception management

## Architecture

### Database Helper Module ([`app/utils/db_helper.py`](../app/utils/db_helper.py))

#### Main Functions

1. **User Management**
   - `create_user(username, email, password)`: Creates a new user account
   - `find_user_by_username(username)`: Finds a user by username
   - `find_user_by_email(email)`: Finds a user by email
   - `update_user_profile(user_id, data)`: Updates user profile information

2. **Admin/Seller Management**
   - `find_admin_seller(username)`: Finds an admin/seller by username
   - `get_all_admin_sellers()`: Retrieves all admin/seller accounts

3. **Product Management**
   - `get_all_products()`: Gets all products from main catalog
   - `get_product_by_id(product_id)`: Finds a product by ID
   - `search_products(query)`: Searches products by description or stock code
   - `add_product(product_data)`: Adds a new product to main catalog
   - `update_product(product_id, updates)`: Updates an existing product
   - `delete_product(product_id)`: Deletes a product from main catalog

4. **Seller Products**
   - `get_seller_products(seller_id)`: Gets products for a specific seller
   - `add_seller_product(seller_id, product_data)`: Adds a product to a seller's catalog
   - `update_seller_product(seller_id, product_id, updates)`: Updates a seller's product
   - `delete_seller_product(seller_id, product_id)`: Deletes a seller's product

5. **Order Management**
   - `create_order(order_data)`: Creates a new order
   - `get_order_by_id(order_id)`: Finds an order by ID
   - `get_orders_by_user(user_id)`: Gets all orders for a specific user
   - `get_orders_by_seller(seller_id)`: Gets all orders for a specific seller

6. **Session Management**
   - `clean_cart_session(cart)`: Cleans and validates cart session data
   - `validate_session_data(session_data)`: Validates session data structure
   - `get_cart_data()`: Helper to get cart data structure

## Database Structure

### Collections

1. **users** - Stores user accounts
   - `_id`: MongoDB ObjectId
   - `username`: User's username (unique)
   - `email`: User's email (unique)
   - `password_hash`: bcrypt hashed password
   - `name`: User's full name
   - `phone_number`: User's phone number
   - `address`: User's address
   - `city`: User's city
   - `state`: User's state
   - `pincode`: User's pincode
   - `profile_image`: URL to user's profile image
   - `role`: User's role (customer, admin_seller)

2. **admin_sellers** - Stores admin and seller accounts
   - `_id`: MongoDB ObjectId
   - `username`: Admin/seller's username (unique)
   - `password_hash`: bcrypt hashed password
   - `name`: Admin/seller's full name
   - `email`: Admin/seller's email
   - `role`: Account role (admin, seller)

3. **products** - Main product catalog
   - `_id`: MongoDB ObjectId
   - `stock_code`: Product stock code
   - `description`: Product description
   - `image_url`: URL to product image
   - `price`: Price in INR
   - `quantity_available`: Number of items available
   - `category`: Product category
   - `brand`: Product brand

4. **seller_products** - Seller-specific products
   - `_id`: MongoDB ObjectId
   - `seller_id`: Admin/seller ID
   - `product_data`: Product information (same structure as products)

5. **orders** - Order information
   - `_id`: MongoDB ObjectId
   - `user_id`: User ID
   - `items`: List of order items
   - `shipping_address`: Shipping details
   - `billing_address`: Billing details
   - `payment_method`: Payment method used
   - `total_amount`: Total order amount
   - `order_date`: Order creation date
   - `status`: Order status (pending, processing, shipped, delivered, cancelled)

## Configuration

### Environment Variables

Set the MongoDB connection string in `.env`:

```env
mongodb_url=mongodb://localhost:27017/shop_smart
```

### Connection Setup

The database connection is established in [`app/extensions.py`](../app/extensions.py):

```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongodb_url = os.getenv('mongodb_url')
client = MongoClient(mongodb_url)
db = client['shop_smart']
```

## Usage Examples

### Creating a User

```python
from app.utils.db_helper import create_user

try:
    user = create_user(
        username="john_doe",
        email="john@example.com",
        password="password123"
    )
    print("User created successfully:", user['_id'])
except Exception as e:
    print(f"Error creating user: {e}")
```

### Finding a Product

```python
from app.utils.db_helper import get_product_by_id

product = get_product_by_id("60d5ec49f1a2c9f7f877bda5")
if product:
    print("Product found:", product['description'])
else:
    print("Product not found")
```

### Creating an Order

```python
from app.utils.db_helper import create_order

order_data = {
    "user_id": "60d5ec49f1a2c9f7f877bda5",
    "items": [
        {
            "product_id": "60d5ec49f1a2c9f7f877bda6",
            "quantity": 2,
            "price": 999.99
        }
    ],
    "shipping_address": "123 Main St, City",
    "billing_address": "123 Main St, City",
    "payment_method": "credit_card",
    "total_amount": 1999.98
}

try:
    order = create_order(order_data)
    print("Order created:", order['_id'])
except Exception as e:
    print(f"Error creating order: {e}")
```

## Data Validation

The database helper includes built-in data validation to ensure consistency:

- All required fields are present
- Product IDs are valid
- Quantities are positive integers
- Prices are valid numbers
- Email addresses are properly formatted

## Error Handling

All database operations include error handling to catch and re-raise exceptions with meaningful messages. Common errors include:

- `ValueError`: Invalid input data
- `Exception`: General database errors

## Performance Considerations

- **Indexes**: Consider adding indexes on frequently queried fields like `username`, `email`, and `category`
- **Batch Operations**: Use batch operations for large datasets
- **Connection Pooling**: MongoDB connection pooling is handled automatically
- **Query Optimization**: Use efficient query patterns to minimize database load

## Future Improvements

- **Data Caching**: Implement caching layer for frequently accessed data
- **Transaction Support**: Add support for multi-document transactions
- **Query Optimization**: Improve query efficiency with advanced MongoDB features
- **Data Backup**: Implement automated backup and restore functionality
- **Connection Management**: Enhance connection pooling and error recovery

## Dependencies

- pymongo
- bcrypt
- python-dotenv
- Flask-Login
