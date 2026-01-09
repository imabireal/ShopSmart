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

