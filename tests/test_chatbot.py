#!/usr/bin/env python3
"""
Test script for chatbot functionality
"""

import requests
import json
import sys

# Base URL of the application
BASE_URL = "http://localhost:5000"

def test_chat_endpoint():
    """Test the chat endpoint with various messages"""
    print("Testing chat endpoint...")
    
    test_messages = [
        "Hello",
        "Recommend some smartphones",
        "Find budget laptops",
        "What about wireless headphones?",
        "Bye"
    ]
    
    for message in test_messages:
        try:
            response = requests.post(f"{BASE_URL}/chat", 
                                  json={"message": message},
                                  timeout=10)
            
            print(f"\nMessage: {message}")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data.get('response')}")
                if 'recommendations' in data and data['recommendations']:
                    print(f"Recommendations: {len(data['recommendations'])} products")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"\nError with message '{message}': {e}")
            return False
    
    return True

def test_clear_chat():
    """Test clearing the chat history"""
    print("\nTesting clear chat endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/chat/clear", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('message')}")
        else:
            print(f"Error: {response.text}")
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

def main():
    """Main test function"""
    print("=== Chatbot Functionality Test ===\n")
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"Server is running (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to server at {BASE_URL}")
        print(f"Please make sure the Flask app is running with 'python run.py'")
        sys.exit(1)
    
    # Run tests
    chat_ok = test_chat_endpoint()
    clear_ok = test_clear_chat()
    
    print("\n" + "="*50)
    if chat_ok and clear_ok:
        print("✅ All chatbot tests passed!")
    else:
        print("❌ Some chatbot tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
