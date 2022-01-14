"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def all_users_list():
    """Shows list of all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user object by its ID"""
    return User.query.get(user_id)

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    
    movie = Movie(title=title, overview=overview,
                    release_date=release_date,
                    poster_path=poster_path)
    
    return movie

def all_movies_list():
    """Shows list of all movies."""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return a movie object by its ID"""
    return Movie.query.get(movie_id)

def rate_a_movie(user, movie, score):
    """Create a new rating for a movie."""

    rating = Rating(score = score,
                    movie = movie,
                    user = user)

    return rating

def get_user_by_email(email):
    """Check if user with email exists.
        If true, return user. 
        If false, return None."""
    
    return User.query.filter(User.email == email).first()

def check_user_password(email, password):
    """If password entered matches password in databse, return True.
        If password does not  match, return False."""
    
    user = User.query.filter(User.email == email).first()

    if user.password == password:
        return user.user_id
    else:
        return False
        


if __name__ == '__main__':
    from server import app
    connect_to_db(app)