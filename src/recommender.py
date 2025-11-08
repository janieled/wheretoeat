"""
Recommender System Module
Simplified recommendation based on vibes and time.
"""

import pandas as pd
from datetime import time as dt_time
from typing import List, Optional
from src.data_loader import DataLoader


class RestaurantRecommender:
    """Simple restaurant recommendation system based on vibes and time."""
    
    def __init__(self, data_loader: DataLoader):
        """
        Initialize the recommender system.
        
        Args:
            data_loader: DataLoader instance with loaded data
        """
        self.data_loader = data_loader
    
    def recommend_by_vibe_and_time(
        self,
        vibes: List[str],
        user_id: int,
        friend_ids: Optional[List[int]] = None,
        selected_time: Optional[dt_time] = None,
        n: int = 10
    ) -> pd.DataFrame:
        """
        Recommend restaurants based on vibes, time, and user preferences.
        
        Args:
            vibes: List of vibes to match
            user_id: The main user's ID
            friend_ids: Optional list of friend user IDs
            selected_time: Optional time for filtering (future enhancement)
            n: Number of recommendations
            
        Returns:
            DataFrame of recommended restaurants
        """
        restaurants_df = self.data_loader.load_restaurants()
        users_df = self.data_loader.load_users()
        
        if not vibes:
            # If no vibes selected, return empty or top N restaurants
            return restaurants_df.head(n)
        
        # Get all user IDs to consider (main user + friends)
        all_user_ids = [user_id]
        if friend_ids:
            all_user_ids.extend(friend_ids)
        
        # Get user preferences
        all_users = users_df[users_df['user_id'].isin(all_user_ids)]
        
        # Collect dietary requirements
        needs_vegan = any(all_users['vegan'] == 'yes')
        needs_vegetarian = any(all_users['vegetarian'] == 'yes')
        needs_nonalcoholic = any(all_users['alcohol'] == 'no')
        
        # Collect allergies
        allergies = []
        for _, user in all_users.iterrows():
            allergy = str(user['allgergies']).strip().lower()
            if allergy and allergy != 'none' and allergy != 'nan':
                allergies.append(allergy)
        
        # Match if any selected vibe is present in the restaurant's vibe list
        def vibe_match(row):
            if not row['vibes'] or len(row['vibes']) == 0:
                return False
            return any(v in row['vibes'] for v in vibes)
        
        # Filter by vibes first
        filtered = restaurants_df[restaurants_df.apply(vibe_match, axis=1)].copy()
        
        # Filter by dietary requirements
        if needs_vegan:
            filtered = filtered[filtered['vegan_options'] == 'Yes']
        if needs_vegetarian:
            filtered = filtered[filtered['vegetarian_options'] == 'Yes']
        if needs_nonalcoholic:
            filtered = filtered[filtered['nonalcoholic_options'] == 'Yes']
        
        # Filter by allergies
        for allergy in allergies:
            if 'peanut' in allergy or 'nut' in allergy:
                filtered = filtered[filtered['nut_allergy_friendly'] == 'Yes']
            elif 'shellfish' in allergy:
                filtered = filtered[filtered['shellfish_allergy_friendly'] == 'Yes']
            elif 'gluten' in allergy:
                filtered = filtered[filtered['glutenfree_options'] == 'Yes']
            elif 'dairy' in allergy or 'lactose' in allergy:
                filtered = filtered[filtered['lactosefree_options'] == 'Yes']
        
        # TODO: Add time-based filtering if needed (e.g., breakfast/lunch/dinner hours)
        # For now, time is just captured but not used for filtering
        
        return filtered.head(n)
