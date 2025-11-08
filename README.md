# 🍽️ WhereToEat - Restaurant Recommendation System

A lightweight MVP restaurant recommendation system built with Streamlit, featuring collaborative filtering and multiple recommendation strategies.

## 🎯 Overview

WhereToEat helps users discover restaurants based on their preferences using:
- **Simple Recommendations**: Average rating-based suggestions
- **Collaborative Filtering**: User-based and item-based recommendations
- **Hybrid Approach**: Combining multiple strategies for better results

## 🏗️ Architecture

### Lightweight MVP Architecture

```
wheretoeat/
├── app.py                  # Main Streamlit application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # Data loading and management
│   └── recommender.py      # Recommendation algorithms
├── data/
│   ├── restaurants.csv     # Restaurant data (20 restaurants)
│   ├── users.csv           # User data (20 users)
│   └── user_reviews.csv    # Review data (100+ reviews)
└── tests/                  # Unit tests (future)
```

### Data Flow

```
Streamlit UI → calls recommender.py → reads data via data_loader.py → outputs ranked recommendations
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/janieled/wheretoeat.git
   cd wheretoeat
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📊 Features

### 1. **Home Page**
- Dataset statistics and overview
- Top-rated restaurants
- Visual insights (cuisine distribution, location analytics)

### 2. **Personalized Recommendations**
- Select a user profile
- Choose recommendation method:
  - User-based Collaborative Filtering
  - Item-based Collaborative Filtering
  - Hybrid Approach
- View past reviews and get tailored suggestions

### 3. **Search & Filter**
- Filter by cuisine type
- Filter by location
- Filter by price range
- Filter by minimum rating
- Sort results by rating, reviews, or name

### 4. **Restaurant Details**
- Detailed restaurant information
- Recent user reviews
- Similar restaurant suggestions

## 🔍 Recommendation Approaches

### 1. Average Rating (Simple)
- Ranks restaurants by average rating
- Considers number of reviews
- Filters by minimum review threshold

### 2. User-Based Collaborative Filtering
- Finds similar users based on rating patterns
- Recommends restaurants liked by similar users
- Uses cosine similarity for user comparison

### 3. Item-Based Collaborative Filtering
- Finds similar restaurants based on user ratings
- Recommends restaurants similar to user's favorites
- Uses cosine similarity for item comparison

### 4. Hybrid Recommendation
- Combines all three approaches
- Weighted scoring (configurable in `config.py`)
- Default weights: 40% user-based, 40% item-based, 20% popularity

## ⚙️ Technology Stack

- **Frontend**: Streamlit (UI framework)
- **Backend**: Python 3.x
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: scikit-learn (cosine similarity)
- **Visualization**: Plotly
- **Data Storage**: CSV files (SQLite support available)

## 📁 Data Schema

### restaurants.csv
- `restaurant_id`: Unique identifier
- `name`: Restaurant name
- `cuisine`: Type of cuisine
- `location`: Restaurant location
- `price_range`: Price category ($, $$, $$$, $$$$)
- `avg_rating`: Average rating (1-5)
- `num_reviews`: Total number of reviews

### users.csv
- `user_id`: Unique identifier
- `username`: User's display name
- `location`: User's location
- `join_date`: Account creation date
- `total_reviews`: Number of reviews written

### user_reviews.csv
- `review_id`: Unique identifier
- `user_id`: Reviewer's ID
- `restaurant_id`: Restaurant being reviewed
- `rating`: Rating (1-5)
- `review_date`: Date of review
- `comment`: Review text

## 🔧 Configuration

Edit `config.py` to customize:
- Number of recommendations
- Collaborative filtering parameters
- Hybrid recommendation weights
- UI settings
- Cache settings

## 📈 Future Enhancements

### Potential Improvements
- **Database Migration**: Move from CSV to PostgreSQL/MongoDB
- **User Authentication**: Add login system
- **Real-time Updates**: Live data updates
- **Advanced Filtering**: More sophisticated filters (dietary restrictions, atmosphere, etc.)
- **ML Models**: Deep learning for recommendations (Neural Collaborative Filtering)
- **API Development**: RESTful API for recommendations
- **Mobile App**: React Native or Flutter mobile version
- **Social Features**: User follows, sharing, wishlists
- **Content-Based Filtering**: Use restaurant attributes (cuisine, location, price) for recommendations

### Scalability Considerations
- Move to client-server architecture
- Implement caching (Redis)
- Add load balancing
- Use message queues for async processing

## 🧪 Testing

Run the data loader test:
```bash
python src/data_loader.py
```

Run the recommender test:
```bash
python src/recommender.py
```

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is an MVP project. Feel free to fork and extend!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Project Link: [https://github.com/janieled/wheretoeat](https://github.com/janieled/wheretoeat)

---

**Built with ❤️ using Streamlit**
Desktop web App to choose where to eat
