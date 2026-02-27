# ShopSmart Chatbot Documentation

## Overview

The ShopSmart chatbot is an AI-powered assistant that helps users find products and get recommendations based on their queries. It uses a Retrieval-Augmented Generation (RAG) approach with Groq API for chat functionality.

## Features

### Core Capabilities
- **Natural Language Understanding**: Handles various types of user queries
- **Product Recommendations**: Suggests relevant products based on user needs
- **Intent Detection**: Identifies user intent (greeting, recommendation, search, help, etc.)
- **Entity Extraction**: Extracts entities like category, brand, price range, and features
- **Real-time Chat**: Interactive chat interface with typing indicators
- **Responsive Design**: Works on both desktop and mobile devices
- **Fallback System**: If Grok API is unavailable, uses a rule-based fallback

## Architecture

### 1. Chatbot Routes ([`app/chatbot/chatbot_routes.py`](../app/chatbot/chatbot_routes.py))
- `/chat`: Handles user messages and returns product recommendations
- `/chat/clear`: Clears chat history from user session

### 2. Chatbot Service ([`app/chatbot/chatbot_service.py`](../app/chatbot/chatbot_service.py))
- **RAG Approach**: Retrieves relevant products based on user query
- **Intent Detection**: Uses regex patterns to identify user intent
- **Entity Extraction**: Extracts products attributes from user messages
- **Product Indexing**: Indexes products by category, brand, keyword, and price range

### 3. Grok API Integration ([`app/chatbot/grok_api.py`](../app/chatbot/grok_api.py))
- **API Client**: Connects to Grok API
- **Context Injection**: Passes product recommendations as context
- **Response Generation**: Generates natural language responses
- **Fallback System**: Falls back to rule-based responses if API fails

### 4. Frontend Interface ([`app/static/js/chatbot.js`](../app/static/js/chatbot.js), [`app/static/css/chatbot.css`](../app/static/css/chatbot.css))
- **Floating Chat Button**: Appears in bottom right corner
- **Chat Window**: Displays messages and recommendations
- **Product Cards**: Shows recommended products with images and prices
- **Animations**: Smooth transitions and typing indicators

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# MongoDB Configuration
mongodb_url=mongodb://localhost:27017/shop_smart

# Flask Configuration
SECRET_KEY=your_secret_key_here
```

See [`/.env.example`](../.env.example) for a template.

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Starting the Application

```bash
python run.py
```

### 2. Accessing the Chatbot

1. Open the home page or product details page
2. Click on the chat button in the bottom right corner
3. Type your query and press Enter or click Send

### Example Queries

- "Hello" - Greeting response
- "Recommend smartphones" - Category-based recommendations
- "Find budget laptops" - Price range search
- "Wireless headphones" - Feature-based search
- "Samsung products" - Brand-specific recommendations
- "What's your help?" - Help information
- "Bye" - Farewell message

## How It Works

### RAG Process

1. **Retrieval**: Extracts entities from user query and retrieves relevant products from database
2. **Context Injection**: Formats products into context for Grok API
3. **Generation**: Grok API generates natural language response based on context
4. **Presentation**: Shows response and product recommendations to user

### Fallback System

If Grok API is unavailable or fails, the chatbot falls back to rule-based responses:
- Uses intent detection
- Generates predefined responses
- Still provides product recommendations

## Customization

### Adding New Intents

Edit `intent_patterns` in [`app/chatbot/chatbot_service.py`](../app/chatbot/chatbot_service.py):

```python
self.intent_patterns = {
    'new_intent': [r'\bpattern1\b', r'pattern2']
}
```

### Customizing Responses

Edit `_generate_response()` method in [`app/chatbot/chatbot_service.py`](../app/chatbot/chatbot_service.py) to add custom responses.

### Modifying Product Indexing

Update `_create_product_index()` method in [`app/chatbot/chatbot_service.py`](../app/chatbot/chatbot_service.py) to add new indexing dimensions.

## Troubleshooting

### Common Issues

1. **Grok API not working**: Check API key and internet connection
2. **No recommendations**: Verify product database contains products
3. **Slow response**: Check API latency or database performance
4. **403 Forbidden**: Check CORS configuration or API access limits

### Debugging

Enable debugging in `run.py`:

```python
app.run(debug=True)
```

Check logs for detailed error information.

## Future Improvements

- **Personalization**: User-specific recommendations based on purchase history
- **Multi-language Support**: Support for multiple languages
- **Advanced Filters**: More detailed product filtering options
- **Analytics**: Track chatbot usage and effectiveness
- **Knowledge Base**: Integration with product documentation and FAQs
