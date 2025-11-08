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
    st.session_state.number = number

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


def save_user_preferences(user_data):
    """Save user preferences to CSV."""
    
    # Check if username already exists
    if user_data['username'] in df['username'].values:
        st.error("Username already exists. Please choose a different username.")
        return False
    
    # Append new user
    with open('data/users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_data.values())
    
    return True

    

def load_users_csv():
    "Load existing users data or create a new CSV if it doesn’t exist."
    if not os.path.exists('data/users.csv'):
        # Create the CSV with headers if it doesn’t exist
        with open('data/users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'phonenumber', 'joined_date',
                             'allergies', 'alcohol', 'vegetarian', 'vegan', 'friend'])
    return pd.read_csv('data/users.csv')

def get_next_user_id(df):
    "Generate the next user ID."
    return df['user_id'].max() + 1 if not df.empty else 1

def save_user_preferences(user_data):
    """Save user preferences to CSV."""
    # Load existing users
    df = load_users_csv()
    
    # Check if username already exists
    if user_data['username'] in df['username'].values:
        st.error("Username already exists. Please choose a different username.")
        return False
    
    # Append new user
    with open('data/users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_data.values())
    
    # Update global users DataFrame
    global users
    users = pd.read_csv('data/users.csv')
    
    return True

def setup_page ():
    st.title("Restaurant Preferences Profile")
    
    # User Information
    st.header("Personal Details")
    username = st.text_input("Username")
    phone_number = st.text_input("Phone Number",value=st.session_state.number or "", help="Format: XXX-XXXX")
    
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
    
    # # Dietary Restrictions
    # vegetarian = st.checkbox("Vegetarian")
    # vegan = st.checkbox("Vegan")
    # Allergies
    dietary_restrictions = st.multiselect(
        "Select any dietary restrictions", 
        [
            "Vegetarian", "Vegan", "Pescatarian", "Kosher", "Halal"
        ]
    )
    
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
        user_id = get_next_user_id(users)
        
        user_data = {
            'user_id': user_id,
            'username': username,
            'phonenumber': phone_number,
            'joined_date': datetime.now().strftime('%Y-%m-%d'),
            'allergies': ';'.join(allergies) if allergies else 'None',
            'alcohol': alcohol_preference,
            'dietary_restriction': ';'.join(dietary_restrictions) if dietary_restrictions else 'None',
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
            st.markdown(f"""
            <div style="line-height: 1.6;">
                <strong>Cuisine:</strong> {restaurant['cuisine']}<br>
                <strong>Location:</strong> {restaurant['location']}<br>
                <strong>Price Range:</strong> {restaurant['price_range']}<br>
                <strong>Vibe:</strong> {restaurant['vibe']}<br>
                <strong>Kid Friendly:</strong> {'Yes' if restaurant['kid_friendly'] == 'Yes' else 'No'}<br>
                <strong>Dog Friendly:</strong> {'Yes' if restaurant['dog_friendly'] == 'Yes' else 'No'}<br>
                <strong>Outdoor Sitting:</strong> {'Yes' if restaurant['outdoor_sitting'] == 'Yes' else 'No'}<br>
                <strong>Happy Hour:</strong> {'Yes' if restaurant['happy_hour'] == 'Yes' else 'No'}<br>
                <strong>Opening Hours:</strong><br>
                - Monday: {restaurant['Monday_opening']} - {restaurant['Monday_closing']}<br>
                - Tuesday: {restaurant['Tuesday_opening']} - {restaurant['Tuesday_closing']}<br>
                - Wednesday: {restaurant['Wednesday_opening']} - {restaurant['Wednesday_closing']}<br>
                - Thursday: {restaurant['Thursday_opening']} - {restaurant['Thursday_closing']}<br>
                - Friday: {restaurant['Friday_opening']} - {restaurant['Friday_closing']}<br>
                - Saturday: {restaurant['Saturday_opening']} - {restaurant['Saturday_closing']}<br>
                - Sunday: {restaurant['Sunday_opening']} - {restaurant['Sunday_closing']}
            </div>
            """, unsafe_allow_html=True)
        # Show predicted rating if available
        if show_predicted_rating:
            if 'predicted_rating' in restaurant:
                st.info(f"🎯 Predicted for you: {restaurant['predicted_rating']:.1f} ⭐")
            elif 'hybrid_score' in restaurant:
                st.info(f"🎯 Match score: {restaurant['hybrid_score']:.2f}")
        
        st.divider()


def main():
    """Main application."""
    # Load data
    loader = load_data()
    recommender = get_recommender(loader)
    
    # Show the combined recommendation page
    show_combined_recommendation(loader, recommender)



# Combined: For You / Group Recommendation Page
def show_combined_recommendation(loader, recommender):
    st.title("👥 For You / Group Recommendation")
    st.markdown("Get recommendations for yourself or with friends!")

    users_df = loader.load_users()
    user_options = users_df[['user_id', 'username']].apply(lambda row: f"{row['username']} (ID: {row['user_id']})", axis=1).tolist()
    # Automatically select the logged-in user
    selected_user = f"{users_df.loc[users_df['phonenumber'] == st.session_state.number, 'username'].values[0]} (ID: {users_df.loc[users_df['phonenumber'] == st.session_state.number, 'user_id'].values[0]})"
    st.write(f"**Logged in as:** {selected_user}")

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
        st.subheader("🎯 Recommendations")
        
        with st.spinner("Finding restaurants..."):
            recommendations = recommender.recommend_by_vibe_and_time(
                vibes=selected_vibes,
                selected_time=selected_time,
                n=5
            )
        
        if len(recommendations) > 0:
            for _, restaurant in recommendations.iterrows():
                display_restaurant_card(restaurant)
        else:
            st.warning("No restaurants found for the selected vibe(s). Try different vibes!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()




# if __name__ == "__main__":
#     main()

if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "setup":
        setup_page()
else:
    main()