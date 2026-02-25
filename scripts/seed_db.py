import csv
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

def seed_database():
    client = MongoClient(os.getenv('mongodb_url'),
                             tlsAllowInvalidCertificates=True)
    db = client["shop_smart"]
    collection = db['products']
    USD_TO_INR_RATE = 96
    data_to_insert = []
    if collection.count_documents({}) == 0:
        try:
            with open('data/Products.csv', mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # 1. Convert price to integer and INR
                    try:
                        row.pop('', None)
                        price_usd = float(row['Price']) # Convert from string in CSV to float
                        price_inr = int(price_usd * USD_TO_INR_RATE) # Convert to INR integer
                        row['price_inr'] = price_inr # Add the new field
                        
                        # Parse JSON fields with proper handling
                        for field in ['features', 'tags', 'attributes', 'image_url']:
                            if field in row:
                                try:
                                    # Replace single quotes with double quotes to make valid JSON
                                    field_value = row[field].replace("'", "\"")
                                    row[field] = json.loads(field_value)
                                except Exception as e:
                                    print(f"Error parsing {field} for product {row.get('title', 'Unknown')}: {e}")
                                    # Set default empty values if parsing fails
                                    if field in ['features', 'tags', 'image_url']:
                                        row[field] = []
                                    elif field == 'attributes':
                                        row[field] = {}
                        
                        # Optional: Convert other fields to their correct types if needed
                        # row['stock_quantity'] = int(row['stock_quantity']) 
                        del row['Price']
                        data_to_insert.append(row)
                    except ValueError:
                        print(f"Skipping row due to invalid price data: {row}")

                # 2. Perform bulk insert
                if data_to_insert and collection.count_documents({}) == 0:
                    collection.insert_many(data_to_insert)
                    print(f"Successfully added {len(data_to_insert)} products with modified prices!")
                elif collection.count_documents({}) > 0:
                    print("Data already exists. Skipping import.")

        except FileNotFoundError:
            print("Error: data.csv not found in the scripts folder.")
    else:
        print("Database already contains data. Skipping import.")

if __name__ == "__main__":
    seed_database()

