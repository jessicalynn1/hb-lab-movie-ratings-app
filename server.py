"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
    """Show homepage"""
    return render_template("homepage.html")


@app.route("/movies")
def show_movies():
    """Show all movies"""

    movies = crud.all_movies_list()

    return render_template("movies.html", movies = movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""
    
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/movies/<movie_id>", methods=["POST"])
def rate_a_movie(movie_id):
    """Allow users to submit a rating to a movie."""
    if session.get('pkey', None) is None:
        flash ("Please log in to rate a movie.")
    else:
        user_id = session['pkey']
        score = int(request.form.get("rating"))
        user = crud.get_user_by_id(user_id)
        movie = crud.get_movie_by_id(movie_id)

        if score not in range(0,6):
            flash("Invalid entry. Try again.")
        else:
            new_rating = crud.rate_a_movie(user, movie, score)
            db.session.add(new_rating)
            db.session.commit()
            flash ("Rating added.")

    return redirect(request.referrer)

@app.route("/users")
def show_users():
    """Show all users"""

    users = crud.all_users_list()

    return render_template("users.html", users = users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    
    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user_exist = crud.get_user_by_email(email)

    if user_exist:
        flash ("This email is already registered on our website. Please log in.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash ("Account created. Please log in.")
    
    return redirect ("/")

@app.route("/login", methods=["POST"])
def log_in():
    """Existing user log in."""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user_exist = crud.get_user_by_email(email)

    if user_exist:
        checked_user = crud.check_user_password(email, password)
        if check_password:
            session['pkey'] = checked_user
            flash ("Success! You are logged in!")
        else:
            flash ("Wrong password. Please try again.")
    else:
        flash ("No match for email entered. Please create an account.")
    
    return redirect ("/")




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
