import pymongo
import bcrypt
import os
from dotenv import load_dotenv
# Load variables from .env into the environment
load_dotenv()

# Mongo db server
client = pymongo.MongoClient(os.getenv('mongodb_url'),
                             tlsAllowInvalidCertificates=True)
db = client["mydatabase"]

def create_user(username, password):
    """Securely registers a new user."""
    users_col = db["users"]
    if users_col.find_one({'username':username}):
        return {
            "success": False,
            "message": "Username already exists"
        }
    # hasing passwords
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Store user in MongoDB
    result = users_col.insert_one({
        "username": username,
        "password": hashed_pw
    })
    
    # Return user data including _id for Flask-Login
    return {
        "success": True,
        "user": {
            "_id": str(result.inserted_id),
            "username": username
        }
    }

def login_user(username, password):
    users_col = db["users"]
    """Authenticates a user against stored records."""
    # Retrieve user document
    user = users_col.find_one({"username": username})
    
    if user:
        # Verify the password against the stored hash
        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            # Return user data including _id for Flask-Login
            return {
                "success": True,
                "user": {
                    "_id": str(user["_id"]),
                    "username": user["username"]
                }
            }
    
    return {
        "success": False,
        "message": "Invalid username or password."
    }

def get_user_by_id(user_id):
    """Fetch user by ID from MongoDB."""
    from bson import ObjectId
    users_col = db["users"]
    try:
        user = users_col.find_one({"_id": ObjectId(user_id)})
        if user:
            return {
                "_id": str(user["_id"]),
                "username": user["username"]
            }
    except:
        pass
    return None

# ==================== PRODUCT DATABASE FUNCTIONS ====================

def get_products():
    """Fetch all main products from database."""
    products_col = db["products"]
    products = list(products_col.find({}, {"_id": 0}))
    return products

def get_products_paginated(page=1, per_page=10):
    """Fetch paginated main products from database.
    
    Args:
        page: Page number (1-indexed)
        per_page: Number of products per page
    
    Returns:
        List of products for the specified page
    """
    products_col = db["products"]
    skip = (page - 1) * per_page
    products = list(products_col.find({}, {"_id": 0}).skip(skip).limit(per_page))
    return products

def count_products():
    """Count total number of main products in database."""
    products_col = db["products"]
    return products_col.count_documents({})

def get_seller_products(seller_username):
    """Fetch products for a specific seller."""
    seller_products_col = db["seller_products"]
    products = list(seller_products_col.find({"seller": seller_username}, {"_id": 0}))
    return products

def get_seller_products_paginated(seller_username, page=1, per_page=10):
    """Fetch paginated seller products from database.
    
    Args:
        seller_username: The seller's username
        page: Page number (1-indexed)
        per_page: Number of products per page
    
    Returns:
        List of products for the specified page
    """
    seller_products_col = db["seller_products"]
    skip = (page - 1) * per_page
    products = list(seller_products_col.find({"seller": seller_username}, {"_id": 0}).skip(skip).limit(per_page))
    return products

def count_seller_products(seller_username):
    """Count total number of seller products in database."""
    seller_products_col = db["seller_products"]
    return seller_products_col.count_documents({"seller": seller_username})

def add_product(name, price):
    """Add a new main product to database."""
    products_col = db["products"]
    # Get next product ID
    last_product = products_col.find_one(sort=[("id", -1)])
    next_id = (last_product["id"] + 1) if last_product else 1

    product = {
        "id": next_id,
        "name": name,
        "price": float(price)
    }
    products_col.insert_one(product)
    return product

def add_seller_product(seller_username, name, price):
    """Add a new seller product to database."""
    seller_products_col = db["seller_products"]
    # Get next seller product ID
    last_product = seller_products_col.find_one(sort=[("id", -1)])
    next_id = (last_product["id"] + 1) if last_product else 101

    product = {
        "id": next_id,
        "name": name,
        "price": float(price),
        "seller": seller_username
    }
    seller_products_col.insert_one(product)
    return product

def update_product(product_id, name, price):
    """Update a main product in database."""
    products_col = db["products"]
    result = products_col.update_one(
        {"id": product_id},
        {"$set": {"name": name, "price": float(price)}}
    )
    return result.modified_count > 0

def update_seller_product(seller_username, product_id, name, price):
    """Update a seller product in database."""
    seller_products_col = db["seller_products"]
    result = seller_products_col.update_one(
        {"id": product_id, "seller": seller_username},
        {"$set": {"name": name, "price": float(price)}}
    )
    return result.modified_count > 0

def delete_product(product_id):
    """Delete a main product from database."""
    products_col = db["products"]
    result = products_col.delete_one({"id": product_id})
    return result.deleted_count > 0

def delete_seller_product(seller_username, product_id):
    """Delete a seller product from database."""
    seller_products_col = db["seller_products"]
    result = seller_products_col.delete_one({"id": product_id, "seller": seller_username})
    return result.deleted_count > 0

def get_product_by_id(product_id):
    """Get a main product by ID."""
    products_col = db["products"]
    # Search by id field (integer)
    try:
        product = products_col.find_one({"StockCode": str(product_id)})
        return product
    except (ValueError, TypeError):
        # If conversion fails, try as string
        return products_col.find_one({"StockCode": str(product_id)}, {"_id": 0})

def get_seller_product_by_id(seller_username, product_id):
    """Get a seller product by ID."""
    seller_products_col = db["seller_products"]
    return seller_products_col.find_one({"id": product_id, "seller": seller_username}, {"_id": 0})

