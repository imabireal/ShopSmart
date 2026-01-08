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
        return "user already exist"
    # hasing passwords
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Store user in MongoDB
    users_col.insert_one({
        "username": username,
        "password": hashed_pw
    })
    return "Registration successful."
def login_user(username, password):
    users_col = db["users"]
    """Authenticates a user against stored records."""
    # Retrieve user document
    user = users_col.find_one({"username": username})
    
    if user:
        # Verify the password against the stored hash
        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return "Login successful!"
    
    return "Invalid username or password."

print(create_user("john_doe", "my_secure_password"))
print(login_user("john_doe", "my_secure_password"))