from app.utils import db_helper
from app.recommender.apriori import recommender
from app.chatbot.grok_api import GrokAPI
import re
import logging

# Set up logging
logger = logging.getLogger('flask-ecommerce')

class ChatbotService:
    """
    Chatbot service for product recommendations using RAG (Retrieval-Augmented Generation) approach
    """
    
    def __init__(self):
        """Initialize chatbot service with necessary data"""
        self.products = db_helper.get_products()
        self.product_index = self._create_product_index()
        self.intent_patterns = self._create_intent_patterns()
        self.grok_api = GrokAPI()
    
    def _create_product_index(self):
        """
        Create an index of products for efficient search
        """
        index = {
            'by_category': {},
            'by_brand': {},
            'by_keyword': {},
            'by_price_range': {
                'budget': {'min': 0, 'max': 500},
                'mid_range': {'min': 500, 'max': 2000},
                'premium': {'min': 2000, 'max': float('inf')}
            }
        }
        
        for product in self.products:
            # Index by category
            category = product.get('category', '').lower()
            if category not in index['by_category']:
                index['by_category'][category] = []
            index['by_category'][category].append(product)
            
            # Index by brand
            brand = product.get('brand', '').lower()
            if brand not in index['by_brand']:
                index['by_brand'][brand] = []
            index['by_brand'][brand].append(product)
            
            # Index by keywords (title, features, tags)
            keywords = set()
            keywords.update(product.get('title', '').lower().split())
            if 'features' in product:
                for feature in product['features']:
                    keywords.update(feature.lower().split())
            if 'tags' in product:
                for tag in product['tags']:
                    keywords.update(tag.lower().split())
            
            for keyword in keywords:
                if keyword not in index['by_keyword']:
                    index['by_keyword'][keyword] = []
                index['by_keyword'][keyword].append(product)
        
        return index
    
    def _create_intent_patterns(self):
        """
        Create intent patterns for understanding user queries
        """
        return {
            'greeting': [r'\b(hi|hello|hey|hii|hola)\b', r'^greetings?$'],
            'recommendation': [r'\brecommend\b', r'\bsuggest\b', r'\bwhat\s+about\b', r'\bcan\s+you\b.*\brecommend\b'],
            'search': [r'\bfind\b', r'\bsearch\b', r'\blook\s+for\b', r'\bwhere\s+can\s+I\s+find\b'],
            'price': [r'\bprice\b', r'\bcost\b', r'\bhow\s+much\b', r'\bbudget\b', r'\bexpensive\b', r'\bcheap\b'],
            'category': [r'\bcategory\b', r'\btype\b', r'\bkind\b', r'\bcategory\b'],
            'brand': [r'\bbrand\b', r'\bcompany\b', r'\bmanufacturer\b'],
            'feature': [r'\bfeature\b', r'\bspecification\b', r'\bspecs\b', r'\bquality\b'],
            'help': [r'\bhelp\b', r'\bassist\b', r'\bwhat\s+can\s+you\b.*\bdo\b', r'\bhow\s+does\b.*\bwork\b'],
            'goodbye': [r'\bbye\b', r'\bgoodbye\b', r'\bsee\s+you\b', r'\bthank\s+you\b']
        }
    
    def _detect_intent(self, message):
        """
        Detect user intent from message
        """
        message = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    return intent
        
        return 'general'
    
    def _extract_entities(self, message):
        """
        Extract entities from user message
        """
        entities = {
            'category': None,
            'brand': None,
            'price_range': None,
            'features': [],
            'keywords': []
        }
        
        # Extract category
        for category in self.product_index['by_category']:
            if category in message.lower():
                entities['category'] = category
                break
        
        # Extract brand
        for brand in self.product_index['by_brand']:
            if brand in message.lower():
                entities['brand'] = brand
                break
        
        # Extract price range
        message_lower = message.lower()
        if any(word in message_lower for word in ['budget', 'cheap', 'affordable']):
            entities['price_range'] = 'budget'
        elif any(word in message_lower for word in ['premium', 'expensive', 'high-end']):
            entities['price_range'] = 'premium'
        elif any(word in message_lower for word in ['mid', 'medium', 'reasonable']):
            entities['price_range'] = 'mid_range'
        
        # Extract features from message
        feature_keywords = ['wireless', 'bluetooth', 'waterproof', 'touchscreen', 'smart', 'digital', 'portable']
        for feature in feature_keywords:
            if feature in message_lower:
                entities['features'].append(feature)
        
        # Extract keywords from message
        entities['keywords'] = [word for word in message.lower().split() if word.isalnum() and len(word) > 2]
        
        return entities
    
    def _retrieve_products(self, entities, limit=5):
        """
        Retrieve products based on extracted entities
        """
        matched_products = []
        
        # Filter by category
        if entities['category']:
            category_products = self.product_index['by_category'].get(entities['category'], [])
            matched_products.extend(category_products)
        
        # Filter by brand
        if entities['brand']:
            brand_products = self.product_index['by_brand'].get(entities['brand'], [])
            matched_products.extend(brand_products)
        
        # Filter by price range
        if entities['price_range']:
            price_range = self.product_index['by_price_range'][entities['price_range']]
            price_products = [
                product for product in self.products
                if price_range['min'] <= product.get('price_inr', 0) <= price_range['max']
            ]
            matched_products.extend(price_products)
        
        # Filter by features
        if entities['features']:
            feature_products = []
            for product in self.products:
                product_features = set()
                if 'features' in product:
                    for feature in product['features']:
                        product_features.update(feature.lower().split())
                if 'tags' in product:
                    product_features.update(tag.lower() for tag in product['tags'])
                
                if all(feature in product_features for feature in entities['features']):
                    feature_products.append(product)
            matched_products.extend(feature_products)
        
        # Filter by keywords
        if entities['keywords']:
            keyword_products = []
            for keyword in entities['keywords']:
                if keyword in self.product_index['by_keyword']:
                    keyword_products.extend(self.product_index['by_keyword'][keyword])
            matched_products.extend(keyword_products)
        
        # If no products matched specific entities, return popular products
        if not matched_products:
            return self.products[:limit]
        
        # Remove duplicates and sort by relevance
        seen = set()
        unique_products = []
        for product in matched_products:
            product_id = product.get('StockCode', str(product.get('_id', '')))
            if product_id not in seen:
                seen.add(product_id)
                unique_products.append(product)
        
        # Sort by number of matches (relevance)
        def get_match_score(product):
            score = 0
            if entities['category'] and entities['category'] in product.get('category', '').lower():
                score += 3
            if entities['brand'] and entities['brand'] in product.get('brand', '').lower():
                score += 3
            if entities['price_range']:
                price_range = self.product_index['by_price_range'][entities['price_range']]
                if price_range['min'] <= product.get('price_inr', 0) <= price_range['max']:
                    score += 2
            if entities['features']:
                product_features = set()
                if 'features' in product:
                    for feature in product['features']:
                        product_features.update(feature.lower().split())
                if 'tags' in product:
                    product_features.update(tag.lower() for tag in product['tags'])
                score += sum(1 for feature in entities['features'] if feature in product_features)
            if entities['keywords']:
                product_text = ' '.join([
                    product.get('title', ''),
                    product.get('category', ''),
                    product.get('brand', ''),
                    ' '.join(product.get('features', [])),
                    ' '.join(product.get('tags', []))
                ]).lower()
                score += sum(1 for keyword in entities['keywords'] if keyword in product_text)
            return score
        
        unique_products.sort(key=get_match_score, reverse=True)
        
        return unique_products[:limit]
    
    def _generate_response(self, intent, entities, products):
        """
        Generate response based on intent, entities, and retrieved products
        """
        responses = {
            'greeting': "Hello! I'm ShopSmart assistant. I can help you find products, recommend items based on your needs, and answer questions about our products. How can I assist you today?",
            'goodbye': "Thank you for chatting! If you have any more questions, feel free to ask. Happy shopping!",
            'help': "I can help you with:\n- Finding products by category, brand, or price range\n- Getting product recommendations based on your needs\n- Answering questions about product features\n- Providing information about our products\n\nWhat would you like help with?",
            'general': "I'm here to help you find products. Could you please be more specific about what you're looking for?",
            'recommendation': self._generate_recommendation_response(entities, products),
            'search': self._generate_search_response(entities, products),
            'price': self._generate_price_response(entities, products),
            'category': self._generate_category_response(entities, products),
            'brand': self._generate_brand_response(entities, products),
            'feature': self._generate_feature_response(entities, products)
        }
        
        return responses.get(intent, responses['general'])
    
    def _generate_recommendation_response(self, entities, products):
        """Generate recommendation response"""
        if products:
            if entities['category']:
                return f"Here are some {entities['category']} products you might like:"
            elif entities['brand']:
                return f"Here are some {entities['brand']} products you might like:"
            elif entities['price_range']:
                price_range = self.product_index['by_price_range'][entities['price_range']]
                return f"Here are some products in your {entities['price_range']} price range:"
            else:
                return "Here are some products you might like:"
        else:
            return "I couldn't find any products matching your preferences. Could you please try different search criteria?"
    
    def _generate_search_response(self, entities, products):
        """Generate search response"""
        if products:
            if entities['category']:
                return f"Here are some {entities['category']} products I found:"
            elif entities['brand']:
                return f"Here are some {entities['brand']} products I found:"
            elif entities['price_range']:
                return f"Here are some products in your price range I found:"
            else:
                return "Here are some products matching your search:"
        else:
            return "I couldn't find any products matching your search. Could you please try different keywords?"
    
    def _generate_price_response(self, entities, products):
        """Generate price response"""
        if products:
            if entities['category']:
                return f"Here are {entities['category']} products with their prices:"
            elif entities['brand']:
                return f"Here are {entities['brand']} products with their prices:"
            else:
                return "Here are some products with their prices:"
        else:
            return "I couldn't find any products matching your price range. Could you please try a different range?"
    
    def _generate_category_response(self, entities, products):
        """Generate category response"""
        if products:
            if entities['category']:
                return f"Here are some products in the {entities['category']} category:"
            else:
                return "Here are some popular product categories you might be interested in:"
        else:
            return "I couldn't find any products in that category. Could you please try a different category?"
    
    def _generate_brand_response(self, entities, products):
        """Generate brand response"""
        if products:
            if entities['brand']:
                return f"Here are some products from {entities['brand']}:"
            else:
                return "Here are some popular brands you might be interested in:"
        else:
            return "I couldn't find any products from that brand. Could you please try a different brand?"
    
    def _generate_feature_response(self, entities, products):
        """Generate feature response"""
        if products:
            if entities['features']:
                features = ', '.join(entities['features'])
                return f"Here are some products with {features} features:"
            else:
                return "Here are some products with popular features:"
        else:
            return "I couldn't find any products with those features. Could you please try different features?"
    
    def get_recommendations(self, message, user_id=None, chat_history=None):
        """
        Main method to get product recommendations based on user query
        """
        chat_history = chat_history or []
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Extract entities
        entities = self._extract_entities(message)
        
        # Retrieve relevant products (RAG retrieval phase)
        products = self._retrieve_products(entities)
        
        # Generate response using Grok API with product context
        response = self.grok_api.generate_response(message, chat_history, products)
        
        return {
            'response': response,
            'recommendations': [
                {
                    'id': str(product.get('_id', product.get('StockCode', ''))),
                    'title': product.get('title', 'Product'),
                    'price': product.get('price_inr', 0),
                    'image_url': product.get('image_url', [''])[0] if product.get('image_url') else '',
                    'category': product.get('category', ''),
                    'brand': product.get('brand', '')
                } for product in products
            ],
            'intent': intent
        }
