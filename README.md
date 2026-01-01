# 🛒 ShopSmart – E-commerce Web Application

ShopSmart is a Flask-based e-commerce web application designed to provide a simple and intuitive online shopping experience. It includes essential e-commerce features such as user authentication, product browsing, shopping cart management, and checkout, with a planned product recommendation system using the **Apriori algorithm**.

---

## Features

- **User Authentication**
  - User registration and login
  - Session-based authentication

- **Product Catalog**
  - Browse available products
  - View product details

- **Shopping Cart**
  - Add products to cart
  - Update product quantities
  - Remove items from cart
  - Session-based cart persistence

- **Buy Now**
  - Instantly purchase a product without adding it to the cart

- **Checkout Process**
  - Secure and streamlined checkout flow

---

## Recommendation System (Planned)

- Product recommendation using the **Apriori algorithm**
- Suggests frequently bought-together products
- Enhances user shopping experience and engagement

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Algorithms:** Apriori (for recommendations – upcoming)
- **Session Management:** Flask sessions

---

## ▶️ Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/imabireal/ShopSmart.git
cd ShopSmart
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the Application
```bash
python app.py
```
---

## TODO / Future Enhancements

- Integrate product recommendation system
- Add database support (MySQL / PostgreSQL / SQLite)
- Improve security (password hashing, CSRF protection)
- Order history and user profiles
- Admin dashboard for product management
- Responsive UI improvement