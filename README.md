# 🛒 ShopSmart – E-commerce Web Application

ShopSmart is a Flask-based e-commerce web application designed to provide a simple and intuitive online shopping experience. It includes essential e-commerce features such as user authentication with secure password hashing, product browsing, shopping cart management, checkout, and an admin/seller dashboard for product management.

---

## Features

### User Authentication
- User registration and login
- Session-based authentication with Flask-Login
- Secure password hashing with bcrypt
- Admin/Seller login with predefined credentials
- Role-based access control (customer, admin_seller)

### Product Catalog
- Browse available products with pagination (12 items per page)
- Search functionality by product description or stock code
- View product details including price in INR
- Main product catalog and seller-specific products

### Shopping Cart
- Add products to cart (requires login)
- Update product quantities
- Remove items from cart
- Session-based cart persistence with data validation
- Cart count displayed in navigation

### Buy Now Functionality
- Instantly purchase a product without adding it to the cart
- Quick checkout option with immediate purchase
- Normal checkout with full payment details

### Checkout Process
- Secure and streamlined checkout flow
- Form validation for payment information
- Card number masking for security
- Support for both cart and buy-now checkout

### Admin/Seller Dashboard
- Admin/Seller login portal
- Dashboard to manage all products
- Add new products to main catalog
- Edit existing products (main and seller-specific)
- Delete products
- View seller-specific products

### Database Integration
- MongoDB database for user storage
- Secure data retrieval and manipulation
- Products stored in MongoDB with CSV seeding support
- Separate collections for main products and seller products

---

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MongoDB (using pymongo)
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Flask-Login
- **Security:** bcrypt for password hashing
- **Session Management:** Flask sessions with data validation
- **Environment Configuration:** python-dotenv

---

## ▶️ Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/imabireal/ShopSmart.git
cd ShopSmart
```

### 2️⃣ Configure Environment Variables
Create a `.env` file in the project root with the following:
```
mongodb_url=your_mongodb_connection_string
SECRET_KEY=your_secret_key
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Seed the Database
Run the seed script to populate the database with sample products:
```bash
python scripts/seed_db.py
```

### 5️⃣ Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

---

## 👥 Admin/Seller Access

Predefined admin/seller credentials:

| Username | Password | Role |
|----------|----------|------|
| admin    | admin123 | Admin |
| superadmin | admin123 | Admin |
| seller1  | seller123 | Seller |
| seller2  | seller123 | Seller |

---

## 📁 Project Structure

```
ShopSmart/
├── app/
│   ├── __init__.py          # Flask app creation and configuration
│   ├── extensions.py        # Flask extensions initialization
│   ├── models/              # User and AdminSeller models
│   ├── routes/              # API routes
│   │   ├── auth_routes.py    # Authentication routes
│   │   ├── product_routes.py # Product catalog and admin routes
│   │   ├── cart_routes.py    # Cart management routes
│   │   └── order_routes.py   # Checkout and order routes
│   ├── utils/               # Utility functions
│   │   ├── db_helper.py      # Database helper functions
│   │   └── utils.py          # Session and validation utilities
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates
│   ├── api/                 # API versioning (v1)
│   ├── chatbot/             # Chatbot functionality
│   ├── recommender/         # Recommendation system (planned)
│   └── services/            # Business logic services
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── scripts/
│   └── seed_db.py           # Database seeding script
├── data/
│   └── products.csv         # Sample product data
├── docs/                    # Documentation
└── tests/                   # Test files
```

---

## 🔧 Key Modules

### Authentication Routes ([auth_routes.py](app/routes/auth_routes.py))
- User login and registration
- Admin/Seller login
- Session management

### Product Routes ([product_routes.py](app/routes/product_routes.py))
- Product catalog display with pagination and search
- Admin/Seller dashboard
- Product management (add, edit, delete)

### Cart Routes ([cart_routes.py](app/routes/cart_routes.py))
- Add/remove items from cart
- Update quantities
- Cart display and management

### Order Routes ([order_routes.py](app/routes/order_routes.py))
- Checkout process
- Buy-now functionality
- Payment processing and validation

### Database Helper ([db_helper.py](app/utils/db_helper.py))
- User and product CRUD operations
- MongoDB connection and queries
- Data validation

### Session Utilities ([utils.py](app/utils/utils.py))
- Session cleaning and validation
- Form data validation
- Card number masking

---

## TODO

- [ ] Add CSRF protection for forms
- [ ] Implement order history
- [ ] Create user profiles
- [ ] Implement product recommendation system (Apriori algorithm)
- [ ] Improve responsive UI design
- [ ] Add email notifications
- [ ] Implement order tracking
- [ ] Enhance product search functionality
- [ ] Implement promotional coupons/discounts
- [ ] Add product reviews and ratings

---

## 📄 License

MIT License - feel free to use this project for learning purposes.
