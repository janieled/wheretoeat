"""
WhereToEat - Restaurant Recommendation App
A Streamlit application for restaurant recommendations using collaborative filtering.
Mobile-first responsive design.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import csv
from datetime import datetime
import os
import plotly.graph_objects as go
from src.data_loader import DataLoader
from src.recommender import RestaurantRecommender

# Page configuration
st.set_page_config(
    page_title="WhereToEat - Restaurant Recommendations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed by default for mobile
)

users = pd.read_csv("data/users.csv")

# --- Session setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "number" not in st.session_state:
    st.session_state.number = None
if "page" not in st.session_state:
    st.session_state.page = "login" 

# --- Login page ---
def login_page():
    st.title("📱 Login")

    number = st.text_input("Phone Number")

    if st.button("Login"):
        user_row = users[users["phonenumber"].astype(str) == number]

        if user_row.empty:
            st.warning("Number not found. Let's set up your account.")
            st.session_state.page = "setup"
            st.session_state.number = number
            st.rerun()
        else:
            # validate password
            st.session_state.logged_in = True
            st.session_state.number = number
            st.session_state.page = "main"
            st.rerun()

# --- Setup page ---
def setup_page():
    st.title("🪄 Account Setup")

    name = st.text_input("Your Name")
    password = st.text_input("Create Password", type="password")

    if st.button("Save and Continue"):
        new_user = pd.DataFrame({
            "number": [st.session_state.number],
            "password": [password],
            "name": [name],
            "role": ["user"]
        })
        # append to CSV
        new_user.to_csv("users.csv", mode="a", header=False, index=False)
        st.success("Account created successfully! Please log in.")
        st.session_state.page = "login"
        st.experimental_rerun()


def load_users_csv():
    """Load existing users data or create a new CSV if it doesn't exist."""
    if not os.path.exists('users.csv'):
        # Create the CSV with headers if it doesn't exist
        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'phonenumber', 'joined_date', 
                             'allergies', 'alcohol', 'vegetarian', 'vegan', 'friend'])
    
    return pd.read_csv('users.csv')

 def save_user_preferences(user_data):
    """Save user preferences to CSV."""
    # Load existing users
    df = load_users_csv()
    
    # Check if username already exists
    if user_data['username'] in df['username'].values:
        st.error("Username already exists. Please choose a different username.")
        return False
    
    # Append new user
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_data.values())
    
    return True

def setup_page    
():
    st.title("Restaurant Preferences Profile")
    
    # User Information
    st.header("Personal Details")
    username = st.text_input("Username")
    phone_number = st.text_input("Phone Number", help="Format: XXX-XXXX")
    
    # Dietary Preferences
    st.header("Dietary Preferences")
    
    # Allergies
    allergies = st.multiselect(
        "Select any food allergies", 
        [
            "None", "Peanuts", "Gluten", "Shellfish", 
            "Dairy", "Eggs", "Soy", "Tree Nuts"
        ]
    )
    
    # Alcohol Preference
    alcohol_preference = st.radio(
        "Do you consume alcohol?", 
        ["Yes", "No"]
    )
    
    # Dietary Restrictions
    vegetarian = st.checkbox("Vegetarian")
    vegan = st.checkbox("Vegan")
    
    # Friends Usernames
    st.header("Social Connections")
    friend_usernames = st.text_input(
        "Friend Usernames", 
        help="Enter friend usernames separated by semicolon (;)"
    )
    
    # Submit Button
    if st.button("Create Profile"):
        # Validate inputs
        if not username or not phone_number:
            st.error("Username and Phone Number are required!")
            return
        
        # Prepare user data
        users_df = load_users_csv()
        user_id = get_next_user_id(users_df)
        
        user_data = {
            'user_id': user_id,
            'username': username,
            'phonenumber': phone_number,
            'joined_date': datetime.now().strftime('%Y-%m-%d'),
            'allergies': ';'.join(allergies) if allergies else 'None',
            'alcohol': alcohol_preference,
            'vegetarian': 'yes' if vegetarian else 'no',
            'vegan': 'yes' if vegan else 'no',
            'friend': friend_usernames or ''
        }
        
        # Attempt to save user data
        if save_user_preferences(user_data):
            st.success(f"Profile created successfully! Your User ID is {user_id}")
            
            # Optional: Show the entered data
            st.write("Your Profile:")
            st.table(pd.DataFrame([user_data]))

if __name__ == '__setup_page':
    setup_page ()

# Mobile-first CSS styling
def inject_mobile_css():
    """Inject custom CSS for mobile-first responsive design."""
    st.markdown("""
        <style>
        /* Mobile-first base styles */
        .main .block-container {
            padding: 1rem 0.5rem;
            max-width: 100%;
        }
        
        /* Improved touch targets */
        button, .stButton button {
            min-height: 44px;
            font-size: 16px;
            padding: 0.5rem 1rem;
        }
        
        /* Better mobile typography */
        h1 {
            font-size: 1.75rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
            line-height: 1.3 !important;
        }
        
        h3 {
            font-size: 1.25rem !important;
        }
        
        /* Restaurant cards - mobile optimized */
        .restaurant-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Metrics - better spacing on mobile */
        .stMetric {
            padding: 0.5rem;
        }
        
        .stMetric label {
            font-size: 0.875rem !important;
        }
        
        .stMetric .metric-value {
            font-size: 1.25rem !important;
        }
        
        /* Selectbox and slider - touch friendly */
        .stSelectbox, .stSlider {
            margin-bottom: 1rem;
        }
        
        /* Expander - better mobile interaction */
        .streamlit-expanderHeader {
            font-size: 1rem !important;
            padding: 0.75rem !important;
        }
        
        /* Plotly charts - responsive */
        .js-plotly-plot {
            width: 100% !important;
        }
        
        /* Sidebar optimization */
        .css-1d391kg {
            padding: 1rem 0.5rem;
        }
        
        /* Radio buttons - vertical stack on mobile */
        .stRadio > div {
            gap: 0.5rem;
        }
        
        /* Dividers - less space on mobile */
        hr {
            margin: 1rem 0 !important;
        }
        
        /* Tablets and larger */
        @media (min-width: 640px) {
            .main .block-container {
                padding: 2rem 1rem;
            }
            
            h1 {
                font-size: 2.25rem !important;
            }
            
            h2 {
                font-size: 1.875rem !important;
            }
            
            .restaurant-card {
                padding: 1.5rem;
            }
        }
        
        /* Desktop */
        @media (min-width: 1024px) {
            .main .block-container {
                padding: 3rem 1rem;
                max-width: 1200px;
            }
            
            h1 {
                font-size: 2.5rem !important;
            }
        }
        
        /* Hide elements on mobile */
        @media (max-width: 640px) {
            .stDeployButton {
                display: none;
            }
        }
        
        /* Improve table readability on mobile */
        table {
            font-size: 0.875rem;
        }
        
        /* Better spacing for columns on mobile */
        [data-testid="column"] {
            padding: 0 0.25rem;
        }
        
        @media (min-width: 640px) {
            [data-testid="column"] {
                padding: 0 0.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)


inject_mobile_css()


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
    """Display a restaurant card with details - mobile optimized."""
    with st.container():
        st.markdown(f"""
            <div class="restaurant-card">
                <h3 style="margin-top: 0;">🍽️ {restaurant['name']}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Mobile-first: Single column on small screens, two columns on larger
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{restaurant['cuisine']}** • {restaurant['location']}")
            st.write(f"💰 {restaurant['price_range']}")
                    
        # Show predicted rating if available
        if show_predicted_rating:
            if 'predicted_rating' in restaurant:
                st.info(f"🎯 Predicted for you: {restaurant['predicted_rating']:.1f} ⭐")
            elif 'hybrid_score' in restaurant:
                st.info(f"🎯 Match score: {restaurant['hybrid_score']:.2f}")
        
        st.divider()


def show_home_page(loader, recommender):
    """Display the home page with top restaurants."""
    st.title("🍽️ WhereToEat")
    st.markdown("Discover your next favorite restaurant!")
    
    # Dataset statistics - mobile optimized (2x2 grid on mobile, 4 columns on desktop)
    stats = loader.get_statistics()
    
    # Create 2 rows of 2 columns for mobile, will expand to 4 on desktop
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    with row1_col1:
        st.metric("🍽️ Restaurants", stats['total_restaurants'])
    with row2_col1:
        st.metric("👥 Users", stats['total_users'])
    
    st.markdown("---")
    
    # Top rated restaurants
    st.subheader("🌟 Top Rated Restaurants")
    
    # Stack controls vertically on mobile for better UX
    n_restaurants = st.slider("Number of Restaurants", 5, 20, 10,
                             help="How many restaurants to show")
    
    
    for _, restaurant in top_restaurants.iterrows():
        display_restaurant_card(restaurant)
    
    # Visualizations - stack vertically on mobile
    st.markdown("---")
    st.subheader("📊 Dataset Insights")
    
    # Cuisine distributionS
    restaurants_df = loader.load_restaurants()
    cuisine_counts = restaurants_df['cuisine'].value_counts()
    fig_cuisine = px.pie(
        values=cuisine_counts.values,
        names=cuisine_counts.index,
        title="Restaurants by Cuisine"
    )
    fig_cuisine.update_layout(height=300)  # Optimize height for mobile
    st.plotly_chart(fig_cuisine, use_container_width=True)
    
    # Location distribution
    location_counts = restaurants_df['location'].value_counts()
    fig_location = px.bar(
        x=location_counts.index,
        y=location_counts.values,
        title="Restaurants by Location",
        labels={'x': 'Location', 'y': 'Count'}
    )
    fig_location.update_layout(height=300)  # Optimize height for mobile
    st.plotly_chart(fig_location, use_container_width=True)


def show_personalized_recommendations(loader, recommender):
    """Display personalized recommendations page."""
    st.title("👤 Personalized")
    st.markdown("Get recommendations based on your taste!")
    
    # User selection - stack vertically on mobile for better UX
    users_df = loader.load_users()
    
    selected_user = st.selectbox(
        "Select User",
        options=users_df['user_id'].tolist(),
        format_func=lambda x: f"User {x} - {users_df[users_df['user_id']==x]['username'].values[0]}",
        help="Choose a user profile to get personalized recommendations"
    )
    
    recommendation_method = st.selectbox(
        "Recommendation Method",
        ["Hybrid", "User-based CF", "Item-based CF"],
        help="Hybrid combines multiple recommendation techniques"
    )
    
    n_recommendations = st.slider("Number of Recommendations", 5, 20, 10,
                                 help="How many recommendations to generate")
    
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
    st.title("🔍 Search & Filter")
    st.markdown("Find restaurants by your preferences!")
    
    # Filters - stack vertically on mobile for better touch interaction
    cuisines = ["All"] + loader.get_unique_cuisines()
    selected_cuisine = st.selectbox("Cuisine", cuisines, 
                                   help="Filter by cuisine type")
    
    locations = ["All"] + loader.get_unique_locations()
    selected_location = st.selectbox("Location", locations,
                                    help="Filter by location")
    
    price_ranges = ["All"] + loader.get_unique_price_ranges()
    selected_price = st.selectbox("Price Range", price_ranges,
                                 help="Filter by price range")
    
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1,
                          help="Show restaurants with at least this rating")
    
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
    st.title("🏪 Details")
    st.markdown("Explore restaurants and find similar options!")
    
    # Restaurant selection
    restaurants_df = loader.load_restaurants()
    
    selected_restaurant_name = st.selectbox(
        "Select Restaurant",
        options=restaurants_df['name'].tolist(),
        help="Choose a restaurant to see details"
    )
    
    restaurant_id = restaurants_df[
        restaurants_df['name'] == selected_restaurant_name
    ]['restaurant_id'].values[0]
    
    restaurant = loader.get_restaurant_by_id(restaurant_id)
    
    # Display restaurant details - mobile optimized
    st.markdown("---")
    
    st.header(f"🍽️ {restaurant['name']}")
    
    # Stack info vertically for mobile
    st.write(f"**Cuisine:** {restaurant['cuisine']}")
    st.write(f"**Location:** {restaurant['location']}")
    st.write(f"**Price:** {restaurant['price_range']}")
    
    # Metrics in row
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⭐ Rating", f"{restaurant['avg_rating']:.1f}")
    with col2:
        st.metric("📝 Reviews", restaurant['num_reviews'])
    
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
                # Mobile-optimized card layout
                st.write(f"**{sim_restaurant['name']}** - {sim_restaurant['avg_rating']:.1f} ⭐")
                st.caption(f"{sim_restaurant['cuisine']} • {sim_restaurant['location']} • {sim_restaurant['price_range']}")
                st.divider()
    else:
        st.info("No similar restaurants found.")


def main():
    """Main application."""
    # Load data
    loader = load_data()
    recommender = get_recommender(loader)
    
    # Sidebar navigation - optimized for mobile
    with st.sidebar:
        st.title("🍽️ WhereToEat")
        page = st.radio(
            "Navigate",
            ["🏠 Home", "� For You/Group", "🔍 Search", "🏪 Details"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        with st.expander("ℹ️ About"):
            st.write(
                "WhereToEat helps you discover great restaurants using "
                "collaborative filtering and ML recommendations."
            )

    # Display selected page
    if page == "🏠 Home":
        show_home_page(loader, recommender)
    elif page == "� For You/Group":
        show_combined_recommendation(loader, recommender)
    elif page == "🔍 Search":
        show_search_filter_page(loader, recommender)
    elif page == "🏪 Details":
        show_restaurant_details(loader, recommender)



# Combined: For You / Group Recommendation Page
def show_combined_recommendation(loader, recommender):
    st.title("👥 For You / Group Recommendation")
    st.markdown("Get recommendations for yourself or with friends!")

    users_df = loader.load_users()
    user_options = users_df[['user_id', 'username']].apply(lambda row: f"{row['username']} (ID: {row['user_id']})", axis=1).tolist()
    selected_user = st.selectbox("Who is going?", user_options, help="Select yourself")

    # Option to add friends
    add_friends = st.checkbox("Add friends?", value=False)
    selected_friends = []
    if add_friends:
        friend_options = [u for u in user_options if u != selected_user]
        selected_friends = st.multiselect("What friends are coming with you?", friend_options, help="Select your friends")

    # Vibe selection
    restaurants_df = loader.load_restaurants()
    # Extract all unique vibes (split by semicolon)
    all_vibes = set()
    for vlist in restaurants_df['vibe'].dropna():
        for v in vlist.split(';'):
            all_vibes.add(v.strip())
    vibes = sorted(all_vibes)
    selected_vibes = st.multiselect("What's the vibe?", vibes, help="Choose one or more vibes for your outing")

    # Date/time selection
    selected_date = st.date_input("Date", help="Pick a date")
    selected_time = st.time_input("Time", help="Pick a time")

    st.markdown("---")
    st.write(f"**User:** {selected_user}")
    st.write(f"**Friends:** {', '.join(selected_friends) if selected_friends else 'None selected'}")
    st.write(f"**Vibe(s):** {', '.join(selected_vibes) if selected_vibes else 'None selected'}")
    st.write(f"**Date/Time:** {selected_date} {selected_time}")

    if st.button("Show Recommendations"):
        # Parse user_id from selected_user string
        user_id = int(selected_user.split("ID: ")[-1].replace(")", ""))
        friend_ids = [int(f.split("ID: ")[-1].replace(")", "")) for f in selected_friends]

        if not add_friends or not selected_friends:
            st.subheader("🎯 Recommended for You")
            n_recommendations = st.slider("Number of Recommendations", 5, 20, 10, help="How many recommendations to generate")
            recommendation_method = st.selectbox(
                "Recommendation Method",
                ["Hybrid", "User-based CF", "Item-based CF"],
                help="Hybrid combines multiple recommendation techniques"
            )
            with st.spinner("Generating recommendations..."):
                if recommendation_method == "User-based CF":
                    recommendations = recommender.recommend_collaborative_user_based(
                        user_id=user_id,
                        n=n_recommendations
                    )
                elif recommendation_method == "Item-based CF":
                    recommendations = recommender.recommend_collabosrative_item_based(
                        user_id=user_id,
                        n=n_recommendations
                    )
                else:  # Hybrid
                    recommendations = recommender.recommend_hybrid(
                        user_id=user_id,
                        n=n_recommendations
                    )
            if len(recommendations) > 0:
                for _, restaurant in recommendations.iterrows():
                    display_restaurant_card(restaurant, show_predicted_rating=True)
            else:
                st.warning("No recommendations available. Try a different method!")
        else:
            st.subheader("🎯 Group Recommendations")
            n_recommendations = st.slider("Number of Group Recommendations", 5, 20, 10, help="How many group recommendations to generate")
            restaurants_df = loader.load_restaurants()
            if selected_vibes:
                # Match if any selected vibe is present in the restaurant's vibe list
                def vibe_match(row):
                    if pd.isna(row['vibe']):
                        return False
                    vibes_in_row = [v.strip() for v in row['vibe'].split(';')]
                    return any(v in vibes_in_row for v in selected_vibes)
                group_recs = restaurants_df[restaurants_df.apply(vibe_match, axis=1)].head(n_recommendations)
            else:
                group_recs = restaurants_df.head(0)
            if len(group_recs) > 0:
                for _, restaurant in group_recs.iterrows():
                    display_restaurant_card(restaurant)
            else:
                st.warning("No group recommendations available for the selected vibe(s).")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()




# if __name__ == "__main__":
#     main()

if not st.session_state.logged_in:
    login_page()
else:
    main()