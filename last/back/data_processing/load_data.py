import os
import pandas as pd
from app import app, db  # Import app and db from the main app module
from models import User, Movie, Rating # Import models

# 数据集路径 (根据用户提供的信息)
DATASET_PATH = r'C:\Users\qiqi\OneDrive\Desktop\work\pythonweb\last\ml-1m'
USERS_FILE = os.path.join(DATASET_PATH, 'users.dat')
MOVIES_FILE = os.path.join(DATASET_PATH, 'movies.dat')
RATINGS_FILE = os.path.join(DATASET_PATH, 'ratings.dat')

def load_users():
    """Loads users from users.dat into the database."""
    print("Loading users...")
    users = pd.read_csv(USERS_FILE, sep='::', engine='python',
                        names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'],
                        encoding='latin-1')
    for index, row in users.iterrows():
        user = User(
            id=row['UserID'],
            gender=row['Gender'],
            age=row['Age'],
            occupation=str(row['Occupation']), # Ensure occupation is string
            zip_code=row['Zip-code']
        )
        db.session.add(user)
    db.session.commit()
    print(f"{len(users)} users loaded.")

def load_movies():
    """Loads movies from movies.dat into the database."""
    print("Loading movies...")
    movies = pd.read_csv(MOVIES_FILE, sep='::', engine='python',
                         names=['MovieID', 'Title', 'Genres'],
                         encoding='latin-1')
    for index, row in movies.iterrows():
        movie = Movie(
            id=row['MovieID'],
            title=row['Title'],
            genres=row['Genres']
        )
        db.session.add(movie)
    db.session.commit()
    print(f"{len(movies)} movies loaded.")

def load_ratings():
    """Loads ratings from ratings.dat into the database."""
    print("Loading ratings...")
    ratings = pd.read_csv(RATINGS_FILE, sep='::', engine='python',
                          names=['UserID', 'MovieID', 'Rating', 'Timestamp'],
                          encoding='latin-1')
    # Consider loading in chunks for large datasets
    count = 0
    batch_size = 10000 # Adjust batch size as needed
    for index, row in ratings.iterrows():
        rating = Rating(
            user_id=row['UserID'],
            movie_id=row['MovieID'],
            rating=row['Rating'],
            timestamp=row['Timestamp']
        )
        db.session.add(rating)
        count += 1
        if count % batch_size == 0:
            db.session.commit()
            print(f"Committed {count}/{len(ratings)} ratings...")

    db.session.commit() # Commit any remaining ratings
    print(f"{len(ratings)} ratings loaded.")

def load_all_data():
    """Loads all data from the ml-1m dataset into the database."""
    with app.app_context(): # Use Flask app context to access db
        print("Dropping existing tables (if any) and creating new ones...")
        # Be cautious with dropping tables in production!
        # db.drop_all()
        db.create_all() # Ensure tables are created based on models
        print("Tables created.")

        # Check if data already exists to avoid duplicates (optional, simple check)
        if User.query.first() or Movie.query.first() or Rating.query.first():
            print("Data seems to exist already. Skipping data loading.")
            print("If you want to reload, please clear the database tables first.")
            return

        try:
            load_users()
            load_movies()
            load_ratings()
            print("Data loading complete.")
        except Exception as e:
            db.session.rollback() # Rollback in case of error
            print(f"An error occurred during data loading: {e}")
            print("Database changes rolled back.")

if __name__ == '__main__':
    print("Starting data loading process...")
    # Make sure the .env file is configured with correct DATABASE_URI
    load_all_data()