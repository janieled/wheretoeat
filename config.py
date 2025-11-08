"""
Configuration file for the WhereToEat application.
Contains application settings and constants.
"""

# Application Settings
APP_NAME = "WhereToEat"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Restaurant Recommendation System using Collaborative Filtering"

# Data Settings
DATA_DIR = "data"
RESTAURANTS_FILE = "restaurants.csv"
USERS_FILE = "users.csv"
REVIEWS_FILE = "user_reviews.csv"
DATABASE_FILE = "restaurants.db"

# Recommendation Settings
DEFAULT_N_RECOMMENDATIONS = 10
DEFAULT_K_NEIGHBORS = 5  # Number of similar users for user-based CF
DEFAULT_K_SIMILAR_ITEMS = 5  # Number of similar items for item-based CF

# Hybrid Recommendation Weights
WEIGHT_USER_CF = 0.4  # User-based collaborative filtering weight
WEIGHT_ITEM_CF = 0.4  # Item-based collaborative filtering weight
WEIGHT_POPULARITY = 0.2  # Popularity-based weight

# Filtering Settings
MIN_REVIEWS_DEFAULT = 5  # Minimum number of reviews for a restaurant to be recommended
MIN_RATING_DEFAULT = 0.0  # Minimum rating filter

# UI Settings
PAGE_ICON = "🍽️"
LAYOUT = "wide"

# Price Range Options
PRICE_RANGES = ["$", "$$", "$$$", "$$$$"]

# Rating Scale
MIN_RATING = 1.0
MAX_RATING = 5.0

# Cache Settings
CACHE_TTL = 3600  # Time to live for cached data in seconds (1 hour)

# Display Settings
MAX_REVIEWS_DISPLAY = 10  # Maximum number of reviews to display per restaurant
MAX_SIMILAR_RESTAURANTS = 5  # Maximum number of similar restaurants to show
