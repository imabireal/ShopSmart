import bcrypt
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def seed_admin_sellers():
    client = MongoClient(os.getenv('mongodb_url'),
                          tlsAllowInvalidCertificates=True)
    db = client["mydatabase"]
    admin_sellers_col = db["admin_sellers"]

    # Check if admin sellers collection is already populated
    if admin_sellers_col.count_documents({}) == 0:
        # Admin users
        admin_users = [
            {"username": "admin", "password": "admin123", "role": "admin"},
            {"username": "superadmin", "password": "admin123", "role": "admin"},
            # Seller users
            {"username": "seller1", "password": "seller123", "role": "seller"},
            {"username": "seller2", "password": "seller123", "role": "seller"}
        ]

        # Hash passwords and insert into database
        for user in admin_users:
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(user["password"].encode('utf-8'), salt)
            
            admin_sellers_col.insert_one({
                "username": user["username"],
                "password": hashed_pw,
                "role": user["role"]
            })
            
            print(f"Created {user['role']}: {user['username']}")

        print("Admin/seller users seeded successfully!")
    else:
        print("Admin/seller users already exist in the database.")

if __name__ == "__main__":
    seed_admin_sellers()
