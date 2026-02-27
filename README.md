# 🛒 ShopSmart – E-commerce Web Application

ShopSmart is a Flask-based e-commerce web application designed to provide a simple and intuitive online shopping experience. It includes essential e-commerce features such as user authentication with secure password hashing, product browsing, shopping cart management, checkout, and an admin/seller dashboard for product management. Additionally, it features a chatbot for customer assistance and a product recommendation system.

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

### Chatbot Integration
- AI-powered chatbot for customer assistance
- Real-time chat interface with message history
- Support for product inquiries, order status, and general questions
- Grok API integration for natural language processing

### Product Recommendation System
- Apriori algorithm for association rule mining
- Generates product recommendations based on customer behavior
- Support for collaborative filtering and association analysis
- Precomputed recommendation rules stored in artifacts

---

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MongoDB (using pymongo)
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Flask-Login
- **Security:** bcrypt for password hashing
- **Session Management:** Flask sessions with data validation
- **Environment Configuration:** python-dotenv
- **Chatbot:** Grok API for natural language processing
- **Recommendation System:** Apriori algorithm for association rule mining
- **Data Analysis:** Pandas for data processing

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
GROK_API_KEY=your_grok_api_key  # Required for chatbot functionality
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Seed the Database
Run the seed script to populate the database with sample products and admin/seller accounts:
```bash
python scripts/seed_db.py
python scripts/seed_admin_sellers.py
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
│   │   ├── order_routes.py   # Checkout and order routes
│   │   └── chatbot_routes.py # Chatbot endpoints
│   ├── utils/               # Utility functions
│   │   ├── db_helper.py      # Database helper functions
│   │   └── utils.py          # Session and validation utilities
│   ├── static/              # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   ├── styles.css    # Main styles
│   │   │   └── chatbot.css   # Chatbot styles
│   │   └── js/
│   │       ├── home.js       # Home page functionality
│   │       ├── buy_now_checkout.js # Buy now checkout
│   │       └── chatbot.js    # Chatbot frontend logic
│   ├── templates/           # HTML templates
│   ├── api/                 # API versioning (v1)
│   ├── chatbot/             # Chatbot functionality
│   │   ├── chatbot_service.py # Chatbot core logic
│   │   └── grok_api.py      # Grok API integration
│   ├── recommender/         # Recommendation system
│   │   └── apriori.py       # Apriori algorithm implementation
│   └── services/            # Business logic services
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── scripts/
│   ├── seed_db.py           # Database seeding script
│   └── seed_admin_sellers.py # Admin/seller account seeding
├── data/
│   └── Products.csv         # Sample product data
├── artifacts/
│   └── apriori_rules-3.pkl  # Precomputed recommendation rules
├── docs/                    # Documentation
│   └── chatbot.md           # Chatbot implementation details
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

### Chatbot Routes ([chatbot_routes.py](app/routes/chatbot_routes.py))
- Chatbot conversation endpoints
- Message history management
- Real-time chat functionality

### Chatbot Service ([chatbot_service.py](app/chatbot/chatbot_service.py))
- Core chatbot logic
- Natural language processing with Grok API
- Product recommendation integration
- Order tracking and customer support

### Grok API Integration ([grok_api.py](app/chatbot/grok_api.py))
- Grok API communication
- Request/response handling
- Error management and retries

### Recommendation System ([apriori.py](app/recommender/apriori.py))
- Apriori algorithm implementation
- Association rule mining
- Product recommendation generation
- Precomputed rules loading and saving

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
- [ ] Improve responsive UI design
- [ ] Add email notifications
- [ ] Implement order tracking
- [ ] Enhance product search functionality
- [ ] Implement promotional coupons/discounts
- [ ] Add product reviews and ratings
- [ ] Improve chatbot response accuracy
- [ ] Add more recommendation algorithms
- [ ] Implement real-time order updates

---

## 📄 License

MIT License - feel free to use this project for learning purposes.
