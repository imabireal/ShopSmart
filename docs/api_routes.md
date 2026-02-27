# ShopSmart API Routes Documentation

## Overview

ShopSmart provides a RESTful API for accessing all e-commerce functionality. The API uses Flask routes with session-based authentication for users and admin/sellers.

## Authentication

### User Authentication

All API endpoints (except login and registration) require user authentication. Authentication is handled through Flask-Login session management.

### Admin/Seller Authentication

Admin and seller endpoints require additional role-based authentication.

## API Routes

### 1. Authentication Routes ([`app/routes/auth_routes.py`](../app/routes/auth_routes.py))

#### User Registration

```
POST /register
```

Request JSON:
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "name": "John Doe",
    "phone_number": "1234567890",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "pincode": "10001"
}
```

Response:
- Success: Redirect to login page
- Error: Error message

#### User Login

```
POST /login
```

Request JSON:
```json
{
    "username": "john_doe",
    "password": "password123"
}
```

Response:
- Success: Redirect to home page
- Error: Error message

#### User Logout

```
GET /logout
```

Response: Redirect to home page

#### Admin/Seller Login

```
POST /admin_seller/login
```

Request JSON:
```json
{
    "username": "admin",
    "password": "admin123"
}
```

Response:
- Success: Redirect to admin/seller dashboard
- Error: Error message

#### Admin/Seller Logout

```
GET /admin_seller/logout
```

Response: Redirect to login page

### 2. Product Routes ([`app/routes/product_routes.py`](../app/routes/product_routes.py))

#### Get All Products (with Pagination)

```
GET /products
```

Query Parameters:
- `page`: Page number (default: 1)
- `search`: Search query (optional)

Response: Rendered HTML template with products

#### Get Product Details

```
GET /product/<product_id>
```

Parameters:
- `product_id`: Product ID (string)

Response: Rendered HTML template with product details

#### Admin/Seller Dashboard

```
GET /admin_seller/dashboard
```

Requires: Admin/Seller authentication

Response: Rendered HTML template with dashboard

#### Add Product (Admin/Seller)

```
POST /admin_seller/add_product
```

Requires: Admin/Seller authentication

Form Data:
- `stock_code`: Stock code
- `description`: Product description
- `price`: Price in INR
- `quantity_available`: Quantity available
- `image_url`: Product image URL
- `category`: Product category
- `brand`: Product brand

Response: Redirect to dashboard with success message

#### Edit Product (Admin/Seller)

```
POST /admin_seller/edit_product/<product_id>
```

Requires: Admin/Seller authentication

Parameters:
- `product_id`: Product ID (string)

Form Data: Same as add product

Response: Redirect to dashboard with success message

#### Delete Product (Admin/Seller)

```
POST /admin_seller/delete_product/<product_id>
```

Requires: Admin/Seller authentication

Parameters:
- `product_id`: Product ID (string)

Response: Redirect to dashboard with success message

### 3. Cart Routes ([`app/routes/cart_routes.py`](../app/routes/cart_routes.py))

#### View Cart

```
GET /cart
```

Requires: User authentication

Response: Rendered HTML template with cart items

#### Add to Cart

```
POST /cart/add
```

Requires: User authentication

Request JSON:
```json
{
    "product_id": "product_id_here",
    "quantity": 1
}
```

Response:
- Success: JSON with cart details
- Error: JSON with error message

#### Update Cart Item

```
POST /cart/update
```

Requires: User authentication

Request JSON:
```json
{
    "product_id": "product_id_here",
    "quantity": 2
}
```

Response:
- Success: JSON with cart details
- Error: JSON with error message

#### Remove from Cart

```
POST /cart/remove
```

Requires: User authentication

Request JSON:
```json
{
    "product_id": "product_id_here"
}
```

Response:
- Success: JSON with cart details
- Error: JSON with error message

### 4. Order Routes ([`app/routes/order_routes.py`](../app/routes/order_routes.py))

#### Checkout (Cart)

```
GET /checkout
```

Requires: User authentication

Response: Rendered HTML template with checkout form

#### Process Checkout

```
POST /checkout
```

Requires: User authentication

Form Data:
- `shipping_address`: Shipping address
- `billing_address`: Billing address
- `card_number`: Credit card number (will be masked)
- `card_expiry`: Card expiry date
- `card_cvv`: Card CVV

Response: Redirect to home page with success message

#### Buy Now Checkout

```
GET /buy_now/<product_id>
```

Requires: User authentication

Parameters:
- `product_id`: Product ID (string)

Response: Rendered HTML template with checkout form

#### Process Buy Now Checkout

```
POST /buy_now/<product_id>
```

Requires: User authentication

Parameters:
- `product_id`: Product ID (string)

Form Data: Same as checkout form

Response: Redirect to home page with success message

### 5. Chatbot Routes ([`app/routes/chatbot_routes.py`](../app/routes/chatbot_routes.py))

#### Send Message

```
POST /chat
```

Requires: User authentication

Request JSON:
```json
{
    "message": "Your question here"
}
```

Response JSON:
```json
{
    "bot_response": "Chatbot response",
    "recommendations": [
        {
            "stock_code": "12345",
            "description": "Product description",
            "price": 999,
            "quantity_available": 10,
            "image_url": "https://example.com/image.jpg",
            "category": "Electronics",
            "brand": "Brand Name"
        }
    ],
    "query": "Your question here",
    "intent": "search"
}
```

#### Clear Chat History

```
GET /chat/clear
```

Requires: User authentication

Response: JSON with confirmation

## Error Handling

All endpoints handle errors appropriately and return meaningful error messages. Common error responses:

```json
{
    "error": "Error description"
}
```

## Response Formats

- HTML responses: Rendered templates for browser access
- JSON responses: For API calls from JavaScript

## Session Management

- Session data is managed using Flask sessions
- Cart data is stored in the session
- Session timeout is configurable

## Rate Limiting

Currently, there is no rate limiting implemented. Consider adding rate limiting for production deployments.

## Security Considerations

- All user passwords are stored using bcrypt hashing
- Card numbers are masked before storage
- Input validation is performed on all form submissions
- SQL injection (or NoSQL injection) protection is implemented

## Future Improvements

- **API Versioning**: Implement API versioning (v1, v2, etc.)
- **Rate Limiting**: Add rate limiting to prevent abuse
- **JWT Authentication**: Support for JWT tokens alongside session-based authentication
- **API Documentation**: Generate Swagger/OpenAPI documentation
- **CORS Configuration**: Allow cross-origin requests from specific domains
- **Request Validation**: Add stricter input validation with schemas
