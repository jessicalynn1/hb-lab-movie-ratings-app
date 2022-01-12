"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
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


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
