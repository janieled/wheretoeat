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
        selected_time: Optional[dt_time] = None,
        n: int = 10
    ) -> pd.DataFrame:
        """
        Recommend restaurants based on vibes and time.
        
        Args:
            vibes: List of vibes to match
            selected_time: Optional time for filtering (future enhancement)
            n: Number of recommendations
            
        Returns:
            DataFrame of recommended restaurants
        """
        restaurants_df = self.data_loader.load_restaurants()
        
        if not vibes:
            # If no vibes selected, return empty or top N restaurants
            return restaurants_df.head(n)
        
        # Match if any selected vibe is present in the restaurant's vibe list
        def vibe_match(row):
            if pd.isna(row['vibe']):
                return False
            vibes_in_row = [v.strip() for v in row['vibe'].split(';')]
            return any(v in vibes_in_row for v in vibes)
        
        # Filter by vibes
        filtered = restaurants_df[restaurants_df.apply(vibe_match, axis=1)]
        
        # TODO: Add time-based filtering if needed (e.g., breakfast/lunch/dinner hours)
        # For now, time is just captured but not used for filtering
        
        return filtered.head(n)
