"""
Recommender System Module
Implements multiple recommendation strategies:
1. Average Rating (Simple)
2. Collaborative Filtering (User-based and Item-based)
3. Hybrid approach combining multiple methods
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Optional, Dict
from src.data_loader import DataLoader


class RestaurantRecommender:
    """Restaurant recommendation system with multiple strategies."""
    
    def __init__(self, data_loader: DataLoader):
        """
        Initialize the recommender system.
        
        Args:
            data_loader: DataLoader instance with loaded data
        """
        self.data_loader = data_loader
        self.user_item_matrix: Optional[pd.DataFrame] = None
        self.user_similarity: Optional[np.ndarray] = None
        self.item_similarity: Optional[np.ndarray] = None
        
    def recommend_by_average_rating(
        self,
        n: int = 10,
        cuisine: Optional[str] = None,
        location: Optional[str] = None,
        price_range: Optional[str] = None,
        min_reviews: int = 5
    ) -> pd.DataFrame:
        """
        Simple recommendation based on average ratings.
        
        Args:
            n: Number of recommendations to return
            cuisine: Filter by cuisine type
            location: Filter by location
            price_range: Filter by price range
            min_reviews: Minimum number of reviews required
            
        Returns:
            DataFrame of top-rated restaurants
        """
        restaurants = self.data_loader.filter_restaurants(
            cuisine=cuisine,
            location=location,
            price_range=price_range
        )
        
        # Filter by minimum reviews
        restaurants = restaurants[restaurants['num_reviews'] >= min_reviews]
        
        # Sort by rating and number of reviews
        recommendations = restaurants.sort_values(
            by=['avg_rating', 'num_reviews'],
            ascending=[False, False]
        ).head(n)
        
        return recommendations
    
    def _build_user_item_matrix(self):
        """Build and cache user-item matrix."""
        if self.user_item_matrix is None:
            self.user_item_matrix = self.data_loader.get_user_item_matrix()
    
    def _calculate_user_similarity(self):
        """Calculate user-user similarity matrix using cosine similarity."""
        self._build_user_item_matrix()
        
        if self.user_similarity is None:
            # Calculate cosine similarity between users
            self.user_similarity = cosine_similarity(self.user_item_matrix)
    
    def _calculate_item_similarity(self):
        """Calculate item-item similarity matrix using cosine similarity."""
        self._build_user_item_matrix()
        
        if self.item_similarity is None:
            # Calculate cosine similarity between items (restaurants)
            # Transpose so restaurants are rows
            self.item_similarity = cosine_similarity(self.user_item_matrix.T)
    
    def recommend_collaborative_user_based(
        self,
        user_id: int,
        n: int = 10,
        k_neighbors: int = 5
    ) -> pd.DataFrame:
        """
        User-based collaborative filtering recommendation.
        Recommends restaurants based on similar users' preferences.
        
        Args:
            user_id: Target user ID
            n: Number of recommendations
            k_neighbors: Number of similar users to consider
            
        Returns:
            DataFrame of recommended restaurants
        """
        self._calculate_user_similarity()
        
        # Get user index in matrix
        try:
            user_idx = self.user_item_matrix.index.get_loc(user_id)
        except KeyError:
            # User not found, return popular recommendations
            return self.recommend_by_average_rating(n=n)
        
        # Get similarity scores for this user
        user_similarities = self.user_similarity[user_idx]
        
        # Get indices of most similar users (excluding the user itself)
        similar_users_indices = np.argsort(user_similarities)[::-1][1:k_neighbors+1]
        
        # Get ratings from similar users
        similar_users_ratings = self.user_item_matrix.iloc[similar_users_indices]
        
        # Calculate weighted average ratings
        weights = user_similarities[similar_users_indices]
        weights = weights.reshape(-1, 1)
        
        # Weighted sum of ratings
        weighted_ratings = (similar_users_ratings * weights).sum(axis=0)
        sum_of_weights = (weights * (similar_users_ratings > 0)).sum(axis=0)
        
        # Avoid division by zero
        predicted_ratings = np.divide(
            weighted_ratings,
            sum_of_weights,
            out=np.zeros_like(weighted_ratings),
            where=sum_of_weights != 0
        )
        
        # Get restaurants the user hasn't rated
        user_ratings = self.user_item_matrix.iloc[user_idx]
        unrated_restaurants = user_ratings[user_ratings == 0].index
        
        # Get predictions for unrated restaurants
        recommendations_dict = {
            'restaurant_id': [],
            'predicted_rating': []
        }
        
        for restaurant_id in unrated_restaurants:
            if restaurant_id in self.user_item_matrix.columns:
                col_idx = self.user_item_matrix.columns.get_loc(restaurant_id)
                pred_rating = predicted_ratings[col_idx]
                if pred_rating > 0:
                    recommendations_dict['restaurant_id'].append(restaurant_id)
                    recommendations_dict['predicted_rating'].append(pred_rating)
        
        # Create DataFrame and sort by predicted rating
        recommendations_df = pd.DataFrame(recommendations_dict)
        
        if len(recommendations_df) == 0:
            return self.recommend_by_average_rating(n=n)
        
        recommendations_df = recommendations_df.sort_values(
            'predicted_rating',
            ascending=False
        ).head(n)
        
        # Merge with restaurant details
        restaurants = self.data_loader.load_restaurants()
        recommendations_df = recommendations_df.merge(
            restaurants,
            on='restaurant_id',
            how='left'
        )
        
        return recommendations_df
    
    def recommend_collaborative_item_based(
        self,
        user_id: int,
        n: int = 10,
        k_similar_items: int = 5
    ) -> pd.DataFrame:
        """
        Item-based collaborative filtering recommendation.
        Recommends restaurants similar to ones the user has liked.
        
        Args:
            user_id: Target user ID
            n: Number of recommendations
            k_similar_items: Number of similar items to consider
            
        Returns:
            DataFrame of recommended restaurants
        """
        self._calculate_item_similarity()
        
        # Get user's ratings
        try:
            user_idx = self.user_item_matrix.index.get_loc(user_id)
        except KeyError:
            return self.recommend_by_average_rating(n=n)
        
        user_ratings = self.user_item_matrix.iloc[user_idx]
        rated_restaurants = user_ratings[user_ratings > 0]
        
        if len(rated_restaurants) == 0:
            return self.recommend_by_average_rating(n=n)
        
        # Calculate predicted ratings for unrated restaurants
        predictions = {}
        unrated_restaurants = user_ratings[user_ratings == 0].index
        
        for unrated_restaurant in unrated_restaurants:
            if unrated_restaurant not in self.user_item_matrix.columns:
                continue
                
            item_idx = self.user_item_matrix.columns.get_loc(unrated_restaurant)
            
            # Get similarity scores for this item
            similarities = self.item_similarity[item_idx]
            
            # Calculate weighted rating based on similar items user has rated
            weighted_sum = 0
            similarity_sum = 0
            
            for rated_restaurant, rating in rated_restaurants.items():
                if rated_restaurant in self.user_item_matrix.columns:
                    rated_idx = self.user_item_matrix.columns.get_loc(rated_restaurant)
                    similarity = similarities[rated_idx]
                    
                    if similarity > 0:
                        weighted_sum += similarity * rating
                        similarity_sum += similarity
            
            if similarity_sum > 0:
                predictions[unrated_restaurant] = weighted_sum / similarity_sum
        
        if len(predictions) == 0:
            return self.recommend_by_average_rating(n=n)
        
        # Sort predictions and get top N
        sorted_predictions = sorted(
            predictions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]
        
        # Create DataFrame
        recommendations_df = pd.DataFrame(
            sorted_predictions,
            columns=['restaurant_id', 'predicted_rating']
        )
        
        # Merge with restaurant details
        restaurants = self.data_loader.load_restaurants()
        recommendations_df = recommendations_df.merge(
            restaurants,
            on='restaurant_id',
            how='left'
        )
        
        return recommendations_df
    
    def recommend_hybrid(
        self,
        user_id: int,
        n: int = 10,
        weight_user_cf: float = 0.4,
        weight_item_cf: float = 0.4,
        weight_popularity: float = 0.2
    ) -> pd.DataFrame:
        """
        Hybrid recommendation combining multiple approaches.
        
        Args:
            user_id: Target user ID
            n: Number of recommendations
            weight_user_cf: Weight for user-based collaborative filtering
            weight_item_cf: Weight for item-based collaborative filtering
            weight_popularity: Weight for popularity-based recommendation
            
        Returns:
            DataFrame of recommended restaurants
        """
        # Get recommendations from different methods
        user_cf = self.recommend_collaborative_user_based(user_id, n=n*2)
        item_cf = self.recommend_collaborative_item_based(user_id, n=n*2)
        popular = self.recommend_by_average_rating(n=n*2)
        
        # Combine scores
        combined_scores = {}
        
        # User-based CF scores
        for _, row in user_cf.iterrows():
            restaurant_id = row['restaurant_id']
            if 'predicted_rating' in row:
                score = row['predicted_rating'] * weight_user_cf
            else:
                score = row['avg_rating'] * weight_user_cf
            combined_scores[restaurant_id] = combined_scores.get(restaurant_id, 0) + score
        
        # Item-based CF scores
        for _, row in item_cf.iterrows():
            restaurant_id = row['restaurant_id']
            if 'predicted_rating' in row:
                score = row['predicted_rating'] * weight_item_cf
            else:
                score = row['avg_rating'] * weight_item_cf
            combined_scores[restaurant_id] = combined_scores.get(restaurant_id, 0) + score
        
        # Popularity scores
        for _, row in popular.iterrows():
            restaurant_id = row['restaurant_id']
            score = row['avg_rating'] * weight_popularity
            combined_scores[restaurant_id] = combined_scores.get(restaurant_id, 0) + score
        
        # Sort by combined score
        sorted_restaurants = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]
        
        # Get restaurant details
        recommendations_df = pd.DataFrame(
            sorted_restaurants,
            columns=['restaurant_id', 'hybrid_score']
        )
        
        restaurants = self.data_loader.load_restaurants()
        recommendations_df = recommendations_df.merge(
            restaurants,
            on='restaurant_id',
            how='left'
        )
        
        return recommendations_df
    
    def get_similar_restaurants(
        self,
        restaurant_id: int,
        n: int = 5
    ) -> pd.DataFrame:
        """
        Find restaurants similar to a given restaurant.
        
        Args:
            restaurant_id: Restaurant ID
            n: Number of similar restaurants to return
            
        Returns:
            DataFrame of similar restaurants
        """
        self._calculate_item_similarity()
        
        if restaurant_id not in self.user_item_matrix.columns:
            return pd.DataFrame()
        
        item_idx = self.user_item_matrix.columns.get_loc(restaurant_id)
        similarities = self.item_similarity[item_idx]
        
        # Get most similar restaurants (excluding itself)
        similar_indices = np.argsort(similarities)[::-1][1:n+1]
        similar_restaurant_ids = self.user_item_matrix.columns[similar_indices]
        
        # Get restaurant details
        restaurants = self.data_loader.load_restaurants()
        similar_restaurants = restaurants[
            restaurants['restaurant_id'].isin(similar_restaurant_ids)
        ].copy()
        
        # Add similarity scores
        similarity_dict = dict(zip(similar_restaurant_ids, similarities[similar_indices]))
        similar_restaurants['similarity_score'] = similar_restaurants['restaurant_id'].map(similarity_dict)
        
        similar_restaurants = similar_restaurants.sort_values('similarity_score', ascending=False)
        
        return similar_restaurants


# Example usage
if __name__ == "__main__":
    # Initialize data loader and recommender
    loader = DataLoader()
    loader.load_all_data()
    
    recommender = RestaurantRecommender(loader)
    
    print("=== Restaurant Recommendation System Demo ===\n")
    
    # 1. Average rating recommendations
    print("1. Top 5 restaurants by average rating:")
    top_rated = recommender.recommend_by_average_rating(n=5)
    for _, restaurant in top_rated.iterrows():
        print(f"   {restaurant['name']} - {restaurant['cuisine']} - Rating: {restaurant['avg_rating']}")
    
    # 2. User-based collaborative filtering
    print("\n2. Recommendations for User 1 (User-based CF):")
    user_cf_recs = recommender.recommend_collaborative_user_based(user_id=1, n=5)
    for _, restaurant in user_cf_recs.iterrows():
        print(f"   {restaurant['name']} - {restaurant['cuisine']}")
    
    # 3. Item-based collaborative filtering
    print("\n3. Recommendations for User 1 (Item-based CF):")
    item_cf_recs = recommender.recommend_collaborative_item_based(user_id=1, n=5)
    for _, restaurant in item_cf_recs.iterrows():
        print(f"   {restaurant['name']} - {restaurant['cuisine']}")
    
    # 4. Hybrid recommendations
    print("\n4. Hybrid recommendations for User 1:")
    hybrid_recs = recommender.recommend_hybrid(user_id=1, n=5)
    for _, restaurant in hybrid_recs.iterrows():
        print(f"   {restaurant['name']} - {restaurant['cuisine']}")
    
    # 5. Similar restaurants
    print("\n5. Restaurants similar to 'The Golden Spoon' (ID: 1):")
    similar = recommender.get_similar_restaurants(restaurant_id=1, n=3)
    for _, restaurant in similar.iterrows():
        print(f"   {restaurant['name']} - {restaurant['cuisine']}")
