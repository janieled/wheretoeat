"""
WhereToEat - Restaurant Recommendation App
A Streamlit application for restaurant recommendations using collaborative filtering.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import DataLoader
from src.recommender import RestaurantRecommender


# Page configuration
st.set_page_config(
    page_title="WhereToEat - Restaurant Recommendations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_data():
    """Load and cache data."""
    loader = DataLoader()
    loader.load_all_data()
    return loader


@st.cache_resource
def get_recommender(_loader):
    """Initialize and cache recommender system."""
    return RestaurantRecommender(_loader)


def display_restaurant_card(restaurant, show_predicted_rating=False):
    """Display a restaurant card with details."""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"🍽️ {restaurant['name']}")
            st.write(f"**Cuisine:** {restaurant['cuisine']}")
            st.write(f"**Location:** {restaurant['location']}")
            st.write(f"**Price Range:** {restaurant['price_range']}")
            
        with col2:
            st.metric("Avg Rating", f"{restaurant['avg_rating']:.1f} ⭐")
            st.caption(f"{restaurant['num_reviews']} reviews")
            
            if show_predicted_rating and 'predicted_rating' in restaurant:
                st.metric("Predicted", f"{restaurant['predicted_rating']:.1f} ⭐")
            elif show_predicted_rating and 'hybrid_score' in restaurant:
                st.metric("Score", f"{restaurant['hybrid_score']:.2f}")
        
        st.divider()


def show_home_page(loader, recommender):
    """Display the home page with top restaurants."""
    st.title("🍽️ WhereToEat - Restaurant Recommendations")
    st.markdown("### Discover your next favorite restaurant!")
    
    # Dataset statistics
    stats = loader.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Restaurants", stats['total_restaurants'])
    with col2:
        st.metric("Total Reviews", stats['total_reviews'])
    with col3:
        st.metric("Active Users", stats['total_users'])
    with col4:
        st.metric("Avg Rating", f"{stats['avg_rating_overall']:.2f} ⭐")
    
    st.markdown("---")
    
    # Top rated restaurants
    st.subheader("🌟 Top Rated Restaurants")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        min_reviews = st.slider("Minimum Reviews", 0, 100, 50, 10)
    with col2:
        n_restaurants = st.slider("Number of Restaurants", 5, 20, 10)
    
    top_restaurants = recommender.recommend_by_average_rating(
        n=n_restaurants,
        min_reviews=min_reviews
    )
    
    for _, restaurant in top_restaurants.iterrows():
        display_restaurant_card(restaurant)
    
    # Visualizations
    st.markdown("---")
    st.subheader("📊 Dataset Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cuisine distribution
        restaurants_df = loader.load_restaurants()
        cuisine_counts = restaurants_df['cuisine'].value_counts()
        fig_cuisine = px.pie(
            values=cuisine_counts.values,
            names=cuisine_counts.index,
            title="Restaurants by Cuisine"
        )
        st.plotly_chart(fig_cuisine, use_container_width=True)
    
    with col2:
        # Location distribution
        location_counts = restaurants_df['location'].value_counts()
        fig_location = px.bar(
            x=location_counts.index,
            y=location_counts.values,
            title="Restaurants by Location",
            labels={'x': 'Location', 'y': 'Count'}
        )
        st.plotly_chart(fig_location, use_container_width=True)


def show_personalized_recommendations(loader, recommender):
    """Display personalized recommendations page."""
    st.title("👤 Personalized Recommendations")
    st.markdown("Get restaurant recommendations based on your preferences!")
    
    # User selection
    users_df = loader.load_users()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_user = st.selectbox(
            "Select User",
            options=users_df['user_id'].tolist(),
            format_func=lambda x: f"User {x} - {users_df[users_df['user_id']==x]['username'].values[0]}"
        )
    
    with col2:
        recommendation_method = st.selectbox(
            "Recommendation Method",
            ["Hybrid", "User-based CF", "Item-based CF"]
        )
    
    n_recommendations = st.slider("Number of Recommendations", 5, 20, 10)
    
    # Display user's past reviews
    with st.expander("📝 Your Past Reviews"):
        user_reviews = loader.get_reviews_by_user(selected_user)
        if len(user_reviews) > 0:
            user_reviews_merged = user_reviews.merge(
                loader.load_restaurants(),
                on='restaurant_id'
            ).sort_values('review_date', ascending=False)
            
            for _, review in user_reviews_merged.head(5).iterrows():
                st.write(f"**{review['name']}** - {review['rating']} ⭐ - {review['review_date'].strftime('%Y-%m-%d')}")
                if review['comment']:
                    st.caption(f"_{review['comment']}_")
        else:
            st.info("No past reviews found.")
    
    st.markdown("---")
    st.subheader("🎯 Recommended for You")
    
    # Generate recommendations
    with st.spinner("Generating recommendations..."):
        if recommendation_method == "User-based CF":
            recommendations = recommender.recommend_collaborative_user_based(
                user_id=selected_user,
                n=n_recommendations
            )
        elif recommendation_method == "Item-based CF":
            recommendations = recommender.recommend_collaborative_item_based(
                user_id=selected_user,
                n=n_recommendations
            )
        else:  # Hybrid
            recommendations = recommender.recommend_hybrid(
                user_id=selected_user,
                n=n_recommendations
            )
    
    if len(recommendations) > 0:
        for _, restaurant in recommendations.iterrows():
            display_restaurant_card(restaurant, show_predicted_rating=True)
    else:
        st.warning("No recommendations available. Try a different method!")


def show_search_filter_page(loader, recommender):
    """Display search and filter page."""
    st.title("🔍 Search & Filter Restaurants")
    st.markdown("Find restaurants based on your preferences!")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cuisines = ["All"] + loader.get_unique_cuisines()
        selected_cuisine = st.selectbox("Cuisine", cuisines)
    
    with col2:
        locations = ["All"] + loader.get_unique_locations()
        selected_location = st.selectbox("Location", locations)
    
    with col3:
        price_ranges = ["All"] + loader.get_unique_price_ranges()
        selected_price = st.selectbox("Price Range", price_ranges)
    
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1)
    
    # Apply filters
    filtered_restaurants = loader.filter_restaurants(
        cuisine=None if selected_cuisine == "All" else selected_cuisine,
        location=None if selected_location == "All" else selected_location,
        price_range=None if selected_price == "All" else selected_price,
        min_rating=min_rating
    )
    
    st.markdown("---")
    st.subheader(f"Found {len(filtered_restaurants)} restaurants")
    
    if len(filtered_restaurants) > 0:
        # Sort options
        sort_by = st.selectbox(
            "Sort by",
            ["Average Rating", "Number of Reviews", "Name"]
        )
        
        if sort_by == "Average Rating":
            filtered_restaurants = filtered_restaurants.sort_values("avg_rating", ascending=False)
        elif sort_by == "Number of Reviews":
            filtered_restaurants = filtered_restaurants.sort_values("num_reviews", ascending=False)
        else:
            filtered_restaurants = filtered_restaurants.sort_values("name")
        
        for _, restaurant in filtered_restaurants.iterrows():
            display_restaurant_card(restaurant)
    else:
        st.info("No restaurants match your criteria. Try adjusting the filters!")


def show_restaurant_details(loader, recommender):
    """Display detailed restaurant information."""
    st.title("🏪 Restaurant Details")
    st.markdown("Explore restaurant details and find similar options!")
    
    # Restaurant selection
    restaurants_df = loader.load_restaurants()
    
    selected_restaurant_name = st.selectbox(
        "Select Restaurant",
        options=restaurants_df['name'].tolist()
    )
    
    restaurant_id = restaurants_df[
        restaurants_df['name'] == selected_restaurant_name
    ]['restaurant_id'].values[0]
    
    restaurant = loader.get_restaurant_by_id(restaurant_id)
    
    # Display restaurant details
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"🍽️ {restaurant['name']}")
        st.write(f"**Cuisine:** {restaurant['cuisine']}")
        st.write(f"**Location:** {restaurant['location']}")
        st.write(f"**Price Range:** {restaurant['price_range']}")
    
    with col2:
        st.metric("Average Rating", f"{restaurant['avg_rating']:.1f} ⭐")
        st.metric("Total Reviews", restaurant['num_reviews'])
    
    # Reviews
    st.markdown("---")
    st.subheader("📝 Recent Reviews")
    
    reviews = loader.get_reviews_by_restaurant(restaurant_id)
    reviews_merged = reviews.merge(
        loader.load_users(),
        on='user_id'
    ).sort_values('review_date', ascending=False)
    
    if len(reviews_merged) > 0:
        for _, review in reviews_merged.head(10).iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{review['username']}** - {review['review_date'].strftime('%Y-%m-%d')}")
                    if review['comment']:
                        st.write(review['comment'])
                with col2:
                    st.write(f"{review['rating']} ⭐")
                st.divider()
    else:
        st.info("No reviews yet.")
    
    # Similar restaurants
    st.markdown("---")
    st.subheader("🔄 Similar Restaurants")
    
    similar_restaurants = recommender.get_similar_restaurants(restaurant_id, n=5)
    
    if len(similar_restaurants) > 0:
        for _, sim_restaurant in similar_restaurants.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{sim_restaurant['name']}**")
                    st.write(f"{sim_restaurant['cuisine']} • {sim_restaurant['location']} • {sim_restaurant['price_range']}")
                with col2:
                    st.metric("Rating", f"{sim_restaurant['avg_rating']:.1f} ⭐")
                st.divider()
    else:
        st.info("No similar restaurants found.")


def main():
    """Main application."""
    # Load data
    loader = load_data()
    recommender = get_recommender(loader)
    
    # Sidebar navigation
    st.sidebar.title("🍽️ Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Personalized Recommendations", "Search & Filter", "Restaurant Details"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "WhereToEat helps you discover great restaurants using "
        "collaborative filtering and machine learning recommendations."
    )
    
    # Display selected page
    if page == "Home":
        show_home_page(loader, recommender)
    elif page == "Personalized Recommendations":
        show_personalized_recommendations(loader, recommender)
    elif page == "Search & Filter":
        show_search_filter_page(loader, recommender)
    elif page == "Restaurant Details":
        show_restaurant_details(loader, recommender)


if __name__ == "__main__":
    main()
