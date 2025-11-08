"""
Data Loader Module
Handles loading and managing restaurant, user, and review data from CSV files.
Provides utility functions for data access and filtering.
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple
import os


class DataLoader:
    """Manages loading and caching of restaurant data."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the DataLoader.
        
        Args:
            data_dir: Directory containing the CSV files
        """
        self.data_dir = Path(data_dir)
        self.restaurants_df: Optional[pd.DataFrame] = None
        self.users_df: Optional[pd.DataFrame] = None
        self.history_df: Optional[pd.DataFrame] = None
        
    def load_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all data files (restaurants, users, reviews).
        
        Returns:
            Tuple of (restaurants_df, users_df, reviews_df)
        """
        self.restaurants_df = self.load_restaurants()
        self.users_df = self.load_users()
        self.history_df = self.load_history()
        
        return self.restaurants_df, self.users_df, self.history_df
    
    def load_restaurants(self) -> pd.DataFrame:
        """Load restaurant data from CSV."""
        if self.restaurants_df is not None:
            return self.restaurants_df
            
        file_path = self.data_dir / "restaurants.csv"
        self.restaurants_df = pd.read_csv(file_path)
        return self.restaurants_df
    
    def load_users(self) -> pd.DataFrame:
        """Load user data from CSV."""
        if self.users_df is not None:
            return self.users_df
            
        file_path = self.data_dir / "users.csv"
        self.users_df = pd.read_csv(file_path)
        self.users_df['join_date'] = pd.to_datetime(self.users_df['join_date'])
        return self.users_df
    
    def load_history(self) -> pd.DataFrame:
        """Load user history data from CSV."""
        if self.history_df is not None:
            return self.history_df

        file_path = self.data_dir / "user_history.csv"
        self.history_df = pd.read_csv(file_path)
        self.history_df['visit_date'] = pd.to_datetime(self.history_df['visit_date'])
        return self.history_df
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[pd.Series]:
        """
        Get restaurant details by ID.
        
        Args:
            restaurant_id: Restaurant ID
            
        Returns:
            Restaurant data as a Series or None if not found
        """
        if self.restaurants_df is None:
            self.load_restaurants()
            
        restaurant = self.restaurants_df[
            self.restaurants_df['restaurant_id'] == restaurant_id
        ]
        
        return restaurant.iloc[0] if len(restaurant) > 0 else None
    
    def get_user_by_id(self, user_id: int) -> Optional[pd.Series]:
        """
        Get user details by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User data as a Series or None if not found
        """
        if self.users_df is None:
            self.load_users()
            
        user = self.users_df[self.users_df['user_id'] == user_id]
        return user.iloc[0] if len(user) > 0 else None
    
    def get_reviews_by_restaurant(self, restaurant_id: int) -> pd.DataFrame:
        """
        Get all reviews for a specific restaurant.
        
        Args:
            restaurant_id: Restaurant ID
            
        Returns:
            DataFrame of reviews for the restaurant
        """
        if self.history_df is None:
            self.load_reviews()
            
        return self.history_df[
            self.history_df['restaurant_id'] == restaurant_id
        ].copy()

    def get_history_by_user(self, user_id: int) -> pd.DataFrame:
        """
        Get all history records by a specific user.

        Args:
            user_id: User ID
            
        Returns:
            DataFrame of history records by the user
        """
        if self.history_df is None:
            self.load_reviews()
            
        return self.history_df[
            self.history_df['user_id'] == user_id
        ].copy()
    
    def filter_restaurants(
        self,
        cuisine: Optional[str] = None,
        location: Optional[str] = None,
        price_range: Optional[str] = None,
        min_rating: float = 0.0
    ) -> pd.DataFrame:
        """
        Filter restaurants by various criteria.
        
        Args:
            cuisine: Filter by cuisine type
            location: Filter by location
            price_range: Filter by price range ($, $$, $$$, $$$$)
            min_rating: Minimum average rating
            
        Returns:
            Filtered DataFrame of restaurants
        """
        if self.restaurants_df is None:
            self.load_restaurants()
            
        filtered_df = self.restaurants_df.copy()
        
        if cuisine:
            filtered_df = filtered_df[filtered_df['cuisine'] == cuisine]
        
        if location:
            filtered_df = filtered_df[filtered_df['location'] == location]
        
        if price_range:
            filtered_df = filtered_df[filtered_df['price_range'] == price_range]
        
        if min_rating > 0:
            filtered_df = filtered_df[filtered_df['avg_rating'] >= min_rating]
        
        return filtered_df
    
    def get_unique_cuisines(self) -> List[str]:
        """Get list of unique cuisines."""
        if self.restaurants_df is None:
            self.load_restaurants()
        return sorted(self.restaurants_df['cuisine'].unique().tolist())
    
    def get_unique_price_ranges(self) -> List[str]:
        """Get list of unique price ranges."""
        if self.restaurants_df is None:
            self.load_restaurants()
        return sorted(self.restaurants_df['price_range'].unique().tolist())
    
    def create_sqlite_db(self, db_path: str = "data/restaurants.db"):
        """
        Export data to SQLite database (optional for future use).
        
        Args:
            db_path: Path to SQLite database file
        """
        # Load all data if not already loaded
        if self.restaurants_df is None:
            self.load_all_data()
        
        # Create SQLite connection
        conn = sqlite3.connect(db_path)
        
        # Write DataFrames to SQLite
        self.restaurants_df.to_sql('restaurants', conn, if_exists='replace', index=False)
        self.users_df.to_sql('users', conn, if_exists='replace', index=False)
        self.history_df.to_sql('reviews', conn, if_exists='replace', index=False)
        
        conn.close()
        print(f"SQLite database created at {db_path}")
    
    def get_user_item_matrix(self) -> pd.DataFrame:
        """
        Create user-item matrix for collaborative filtering.
        Rows are users, columns are restaurants, values are ratings.
        
        Returns:
            DataFrame with users as rows and restaurants as columns
        """
        if self.history_df is None:
            self.load_reviews()
        
        # Create pivot table
        user_item_matrix = self.history_df.pivot_table(
            index='user_id',
            columns='restaurant_id',
            fill_value=0
        )
        
        return user_item_matrix
    
    def get_statistics(self) -> dict:
        """
        Get summary statistics about the dataset.
        
        Returns:
            Dictionary with dataset statistics
        """
        if self.restaurants_df is None:
            self.load_all_data()
        
        stats = {
            'total_restaurants': len(self.restaurants_df),
            'total_users': len(self.users_df),
            'total_reviews': len(self.history_df),
            'cuisines': self.restaurants_df['cuisine'].nunique(),
        }
        
        return stats


# Example usage
if __name__ == "__main__":
    # Initialize data loader
    loader = DataLoader()
    
    # Load all data
    restaurants, users, reviews = loader.load_all_data()
    
    print("Data loaded successfully!")
    print(f"\nRestaurants: {len(restaurants)}")
    print(f"Users: {len(users)}")
    print(f"Reviews: {len(reviews)}")
    
    # Get statistics
    stats = loader.get_statistics()
    print(f"\nDataset Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Example: Filter restaurants
    italian_restaurants = loader.filter_restaurants(cuisine="Italian", min_rating=4.0)
    print(f"\nItalian restaurants with rating >= 4.0: {len(italian_restaurants)}")
    
    # Create SQLite database (optional)
    # loader.create_sqlite_db()
