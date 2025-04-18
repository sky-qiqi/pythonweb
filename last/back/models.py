from extensions import db # <- Change this line
# from app import db <- Remove this line

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add other user fields as needed, e.g., age, gender, occupation from ml-1m
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    occupation = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    ratings = db.relationship('Rating', backref='user', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genres = db.Column(db.String(255)) # Store genres as a pipe-separated string or use a separate table
    # Add other movie fields if necessary
    ratings = db.relationship('Rating', backref='movie', lazy=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer) # Store timestamp from ml-1m

    def __repr__(self):
        return f'<Rating {self.user_id} {self.movie_id} {self.rating}>'