import os
import logging
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger('flask-ecommerce')

class GrokAPI:
    """
    Grok API integration for chat functionality using the official Python SDK
    """
    
    def __init__(self):
        """Initialize Grok API client"""
        self.api_key = os.getenv('GROQ_API_KEY')
        self.model = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
        
        if not self.api_key:
            logger.warning('GROQ_API_KEY not configured. Chat functionality will be limited.')
            self.client = None
        else:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {str(e)}")
                self.client = None
    
    def is_available(self):
        """Check if Grok API is available"""
        return self.client is not None
    
    def generate_response(self, message, chat_history, products):
        """
        Generate response using Grok API with product recommendations
        """
        if not self.is_available():
            return self._fallback_response(message, products)
        
        try:
            # Prepare context with products
            products_context = self._format_products_context(products)
            
            # Prepare chat history
            history = []
            for msg in chat_history:
                history.append({'role': 'user', 'content': msg['user']})
                history.append({'role': 'assistant', 'content': msg['bot']})
            
            # Prepare system prompt
            system_prompt = """You are ShopSmart assistant, an AI assistant for an e-commerce platform. 
Your role is to help users find products they're looking for and make recommendations based on their needs.

Key Responsibilities:
1. Provide helpful and friendly responses to user queries
2. Recommend products based on user needs
3. Answer questions about products
4. Help users find specific products
5. Guide users through the shopping experience

Response Guidelines:
- Be professional and friendly
- Keep responses concise and helpful
- Focus on product recommendations
- Include relevant product information
- Guide users to product pages

Available Products:
{products_context}

Please respond to the user's query based on the available products and your knowledge of the e-commerce platform.
""".format(products_context=products_context)
            
            # Prepare the messages
            messages = [
                {
                    'role': 'system',
                    'content': system_prompt
                }
            ] + history + [
                {
                    'role': 'user',
                    'content': message
                }
            ]
            
            # Make the API request
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=1000
            )
            
            return chat_completion.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Grok API exception: {str(e)}", exc_info=True)
            return self._fallback_response(message, products)
    
    def _format_products_context(self, products):
        """
        Format products for context injection
        """
        if not products:
            return "No products available for recommendations at the moment."
        
        product_info = []
        for i, product in enumerate(products, 1):
            info = f"{i}. {product.get('title', 'Product')}"
            info += f" - ₹{product.get('price_inr', 0)}"
            if product.get('category'):
                info += f" ({product.get('category')})"
            if product.get('brand'):
                info += f" by {product.get('brand')}"
            
            product_info.append(info)
        
        return "\n".join(product_info)
    
    def _fallback_response(self, message, products):
        """
        Fallback response if Grok API is not available
        """
        from app.chatbot.chatbot_service import ChatbotService
        
        fallback_service = ChatbotService()
        intent = fallback_service._detect_intent(message)
        entities = fallback_service._extract_entities(message)
        return fallback_service._generate_response(intent, entities, products)
