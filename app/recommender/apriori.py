import pandas as pd
import joblib
import logging
from typing import List, Optional

# Set up logging
logger = logging.getLogger('flask-ecommerce')
logger.setLevel(logging.INFO)

class ProductRecommender:
    def __init__(self, rules_path="artifacts/apriori_rules-3.pkl"):
        # Load the saved rules
        try:
            self.rules = joblib.load(rules_path)
            logger.info(f"Apriori rules loaded successfully from {rules_path}")
            logger.info(f"Number of rules loaded: {len(self.rules)}")
        except Exception as e:
            logger.error(f"Error loading Apriori rules: {e}")
            self.rules = pd.DataFrame()
        
    def get_recommendations(self, product_names: List[str], top_n: int = 5, min_lift: float = 1.0) -> List[str]:
        """
        Get product recommendations based on one or more input products
        
        Args:
            product_names: List of product names to base recommendations on
            top_n: Number of recommendations to return
            min_lift: Minimum lift threshold for recommendations
            
        Returns:
            List of recommended product names
        """
        if self.rules.empty:
            logger.warning("No Apriori rules available for recommendations")
            return []
            
        if not product_names:
            logger.warning("No product names provided for recommendations")
            return []
            
        # Clean and validate input product names
        product_names = [name.strip() for name in product_names if name and name.strip()]
        if not product_names:
            logger.warning("No valid product names provided after cleaning")
            return []
            
        logger.info(f"Generating recommendations for products: {product_names}")
        
        # Filter rules where any of the products are in the antecedent
        mask = pd.Series([False] * len(self.rules))
        for product_name in product_names:
            product_mask = self.rules["antecedents"].str.contains(product_name, case=False, regex=False)
            mask = mask | product_mask
            
        recommendations = self.rules[mask]
        
        # Apply lift threshold
        recommendations = recommendations[recommendations["lift"] >= min_lift]
        
        if recommendations.empty:
            logger.info(f"No recommendations found for products: {product_names}")
            return []
            
        # Sort by lift (descending) and then by confidence (descending)
        recommendations = recommendations.sort_values(by=["lift", "confidence"], ascending=[False, False])
        
        # Collect unique consequents, excluding the input products
        unique_recommendations = []
        for product in recommendations["consequents"].unique():
            if product not in product_names:
                unique_recommendations.append(product)
                if len(unique_recommendations) >= top_n:
                    break
        
        logger.info(f"Generated {len(unique_recommendations)} recommendations: {unique_recommendations}")
        return unique_recommendations
        
    def get_cart_recommendations(self, cart_items: List[dict], top_n: int = 5, min_lift: float = 1.0) -> List[str]:
        """
        Get recommendations based on items in the shopping cart
        
        Args:
            cart_items: List of cart items with 'title' field
            top_n: Number of recommendations to return
            min_lift: Minimum lift threshold for recommendations
            
        Returns:
            List of recommended product names
        """
        product_names = [item.get('title', '') for item in cart_items if item.get('title')]
        return self.get_recommendations(product_names, top_n, min_lift)
        
    def get_popular_products(self, top_n: int = 5) -> List[str]:
        """
        Get popular products as fallback recommendations
        
        Args:
            top_n: Number of popular products to return
            
        Returns:
            List of popular product names
        """
        # For fallback recommendations, we can use products that appear most frequently in consequents
        if self.rules.empty:
            logger.warning("No rules available for popular products fallback")
            return []
            
        try:
            # Get product frequencies from consequents
            product_counts = self.rules["consequents"].value_counts()
            popular_products = product_counts.head(top_n).index.tolist()
            logger.info(f"Popular products fallback: {popular_products}")
            return popular_products
        except Exception as e:
            logger.error(f"Error getting popular products: {e}")
            return []
            
    def get_related_products(self, product_name: str, top_n: int = 5, min_lift: float = 1.0) -> List[str]:
        """
        Get related products for a single product (simplified interface)
        
        Args:
            product_name: Product name to find related products for
            top_n: Number of recommendations to return
            min_lift: Minimum lift threshold for recommendations
            
        Returns:
            List of related product names
        """
        return self.get_recommendations([product_name], top_n, min_lift)

# Singleton instance for application use
recommender = ProductRecommender()