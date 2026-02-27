# ShopSmart Recommendation System Documentation

## Overview

The ShopSmart recommendation system uses the Apriori algorithm for association rule mining to suggest products to users based on their behavior. It analyzes product co-occurrences in orders to identify patterns and generate relevant recommendations.

## Features

- **Association Rule Mining**: Uses Apriori algorithm to find frequent itemsets and association rules
- **Precomputed Rules**: Stores precomputed rules in a pickle file for fast access
- **Product Recommendations**: Generates product recommendations based on current cart items
- **Support for Minimum Support and Confidence**: Configurable parameters for rule generation
- **Rule Loading/Saving**: Supports loading rules from file and saving new rules

## Architecture

### Recommendation Module ([`app/recommender/apriori.py`](../app/recommender/apriori.py))

#### Key Classes and Methods

1. **Apriori class**: Main class implementing the Apriori algorithm
   - `__init__(self, min_support=0.01, min_confidence=0.1)`: Initializes with minimum support and confidence
   - `fit(self, transactions)`: Trains the model on transaction data
   - `_generate_frequent_itemsets(self, transactions)`: Generates frequent itemsets
   - `_generate_association_rules(self)`: Generates association rules from frequent itemsets
   - `predict(self, items)`: Predicts recommended items based on given items
   - `get_recommendations_with_scores(self, items)`: Returns recommendations with confidence scores

2. **RuleManager class**: Manages loading and saving of association rules
   - `save_rules(rules, filename)`: Saves rules to a file
   - `load_rules(filename)`: Loads rules from a file

## Configuration

### Parameters

In `apriori.py`, you can configure the following parameters:

```python
min_support = 0.01  # Minimum support for frequent itemsets (1% of transactions)
min_confidence = 0.1  # Minimum confidence for association rules (10%)
```

### Rule File Location

Precomputed rules are stored in:
```
artifacts/apriori_rules-3.pkl
```

## Usage

### Training the Recommendation System

```python
from app.recommender.apriori import Apriori, RuleManager

# Load transaction data (list of lists)
transactions = [
    ['product1', 'product2', 'product3'],
    ['product1', 'product2'],
    ['product3', 'product4'],
    # more transactions...
]

# Initialize Apriori algorithm
apriori = Apriori(min_support=0.01, min_confidence=0.1)

# Train on transactions
apriori.fit(transactions)

# Save rules to file
RuleManager.save_rules(apriori.rules, 'artifacts/apriori_rules.pkl')
```

### Generating Recommendations

```python
from app.recommender.apriori import Apriori, RuleManager

# Load precomputed rules
rules = RuleManager.load_rules('artifacts/apriori_rules.pkl')
apriori = Apriori()
apriori.rules = rules

# Get recommendations for a product
recommendations = apriori.predict(['product1'])
print("Recommendations for product1:", recommendations)

# Get recommendations with confidence scores
recommendations_with_scores = apriori.get_recommendations_with_scores(['product1'])
for product, score in recommendations_with_scores:
    print(f"Product: {product}, Confidence: {score:.2f}")
```

## How It Works

### Apriori Algorithm Process

1. **Transaction Collection**: Gathers order data from the database
2. **Frequent Itemsets Generation**: Identifies itemsets that appear in a minimum percentage of transactions
3. **Association Rule Generation**: Creates rules from frequent itemsets based on minimum confidence
4. **Recommendation**: Uses rules to predict complementary products for given items

### Calculating Recommendations

When a user adds a product to their cart, the system:
1. Extracts current items in the cart
2. Finds association rules where the antecedent matches the current items
3. Collects all consequent items from matching rules
4. Ranks recommendations by confidence score
5. Returns top recommendations to the user

## Customization

### Adjusting Recommendation Parameters

Modify the parameters in `apriori.py`:

```python
# Increase minimum support to get more frequent itemsets (but fewer rules)
apriori = Apriori(min_support=0.02, min_confidence=0.1)

# Increase minimum confidence to get more reliable rules (but fewer recommendations)
apriori = Apriori(min_support=0.01, min_confidence=0.15)
```

### Retraining the Model

To retrain the recommendation system with new data:

1. Collect all order items from the database
2. Convert to transaction format
3. Train the Apriori algorithm
4. Save the new rules to replace the existing file

## Troubleshooting

### No Recommendations

- Check if the rules file exists and is readable
- Verify that there are enough transactions to generate rules
- Adjust minimum support and confidence parameters

### Low-Quality Recommendations

- Increase minimum support to get more frequent itemsets
- Increase minimum confidence to get more reliable rules
- Ensure transaction data is representative of user behavior

### Performance Issues

- Ensure rules file is properly precomputed and saved
- Avoid retraining the model on large datasets in real-time
- Consider caching frequent recommendations

## Future Improvements

- **Collaborative Filtering**: Add user-based and item-based collaborative filtering
- **Hybrid Systems**: Combine association rule mining with collaborative filtering
- **Real-time Updates**: Implement incremental rule generation
- **Personalization**: Consider user preferences and purchase history
- **Context Awareness**: Incorporate contextual information (time, location, etc.)
- **Performance Optimization**: Optimize Apriori algorithm for large datasets

## Dependencies

- pandas
- numpy
- pickle
