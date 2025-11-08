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
import random
from datetime import datetime, timedelta

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
    """Display a restaurant card with details - single column layout."""
    with st.container():

        points = int(restaurant['points']) if pd.notna(restaurant['points']) else 0
        st.markdown(f"""
        <div class="restaurant-card">
            <h3 style="margin-top: 0;">🍽️ {restaurant['name']} ({points} points)</h3>
            <div style="line-height: 1.6;">
            {', '.join(restaurant['vibes'])} | {restaurant['cuisine']} | {restaurant['location']} | {restaurant['price_range']}
            </div>
        </div>
        """, unsafe_allow_html=True)



def main():
    """Main application."""
    # Load data
    loader = load_data()
    recommender = get_recommender(loader)
    
    # Show the combined recommendation page
    show_combined_recommendation(loader, recommender)



# Combined: For You / Group Recommendation Page
def show_combined_recommendation(loader, recommender):
    st.title("See you soon!")

    users_df = loader.load_users()
    # Automatically select the logged-in user
    current_user_row = users_df.loc[users_df['phonenumber'] == st.session_state.number]
    selected_user = current_user_row['username'].values[0]
    current_user_id = current_user_row['user_id'].values[0]
    st.write(f"Hey, {selected_user}!")
    st.divider()

    # Vibe selection
    restaurants_df = loader.load_restaurants()
    # Only include vibes that have at least one restaurant
    all_vibes = restaurants_df['vibes'].explode().dropna()
    vibes = sorted([v for v in all_vibes.unique().tolist() if len(restaurants_df[restaurants_df['vibes'].apply(lambda x: v in x)]) > 0])
    selected_vibes = st.multiselect("What's the vibe?", vibes, help="Choose one or more vibes for your outing")
    st.divider()
    
    # Option to add friends - only show user's actual friends
    friend_ids_str = current_user_row['friend'].values[0]
    if pd.notna(friend_ids_str) and friend_ids_str:
        friend_ids = [int(fid.strip()) for fid in str(friend_ids_str).split(';')]
        friend_options = users_df[users_df['user_id'].isin(friend_ids)]['username'].tolist()
    else:
        friend_options = []
    
    selected_friends = st.multiselect("Are you bringing friends?", friend_options, help="Select your friends")
    st.divider()

    # Date/time selection
    selected_date = st.date_input("Date", help="Pick a date")
    # Calculate the next half hour from now
    now = datetime.now()
    next_half_hour = (now + timedelta(minutes=30)).replace(second=0, microsecond=0)
    next_half_hour = next_half_hour.replace(minute=(next_half_hour.minute // 30) * 30)

    selected_time = st.time_input("Time", value=next_half_hour.time(), help="Pick a time")

    st.divider()

    if st.button("Show Recommendations"):
        st.subheader("🎯 Recommendations")
        
        # Get friend IDs from selected friend names
        friend_user_ids = []
        if selected_friends:
            friend_user_ids = users_df[users_df['username'].isin(selected_friends)]['user_id'].tolist()
        
        with st.spinner("Will we see you soon?"):
            recommendations = recommender.recommend_by_vibe_and_time(
                vibes=selected_vibes,
                user_id=current_user_id,
                friend_ids=friend_user_ids if friend_user_ids else None,
                selected_time=selected_time,
                n=3
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