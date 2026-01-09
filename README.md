# 🛒 ShopSmart – E-commerce Web Application

ShopSmart is a Flask-based e-commerce web application designed to provide a simple and intuitive online shopping experience. It includes essential e-commerce features such as user authentication with secure password hashing, product browsing, shopping cart management, and checkout, with a planned product recommendation system using the **Apriori algorithm**.

---

## Features

- **User Authentication**
  - User registration and login
  - Session-based authentication with Flask-Login
  - Secure password hashing with bcrypt

- **Product Catalog**
  - Browse available products
  - View product details

- **Shopping Cart**
  - Add products to cart
  - Update product quantities
  - Remove items from cart
  - Session-based cart persistence with data validation

- **Buy Now**
  - Instantly purchase a product without adding it to the cart

- **Checkout Process**
  - Secure and streamlined checkout flow
  - Form validation for payment information
  - Card number masking for security

- **Database Integration**
  - MongoDB database for user storage
  - Secure data retrieval and manipulation

---

## Recommendation System (Planned)

- Product recommendation using the **Apriori algorithm**
- Suggests frequently bought-together products
- Enhances user shopping experience and engagement

---

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MongoDB (using pymongo)
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Flask-Login
- **Security:** bcrypt for password hashing
- **Session Management:** Flask sessions with data validation

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

### 4️⃣ Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## Project Structure

```
ShopSmart/
├── app.py              # Main Flask application
├── db_helper.py        # Database helper functions
├── utils.py            # Utility functions for session management
├── models.py           # Data models
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (create this)
├── .gitignore          # Git ignore rules
├── static/
│   ├── styles.css      # Global styles
│   └── js/
│       ├── home.js             # Home page JavaScript
│       └── buy_now_checkout.js # Buy now checkout JavaScript
└── templates/
    ├── home.html              # Home page template
    ├── login.html             # Login page template
    ├── register.html          # Registration page template
    ├── cart.html              # Shopping cart template
    └── buy_now_checkout.html  # Buy now checkout template
```

---

## TODO

- [ ] Add CSRF protection for forms
- [ ] Implement order history
- [ ] Create user profiles
- [ ] Build admin dashboard for product management
- [ ] Implement product recommendation system (Apriori algorithm)
- [ ] Improve responsive UI design
- [ ] Add email notifications
- [ ] Implement order tracking
- [ ] Add product search functionality
- [ ] Implement promotional coupons/discounts

