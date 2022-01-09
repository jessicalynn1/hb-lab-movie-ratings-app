"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []

#movie_data = [{'overview': 'The near future, [...] search of the unknown.',
#'poster_path': 'https://image.tmdb.org/t/p/original//xBHvZcjRiWyobQ9kxBhO6B2dtRI.jpg',
#'release_date': '2019-09-20',
#'title': 'Ad Astra'}......]

for movie in movie_data:
    # Get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']
    release_date = datetime.strptime(movie['release_date'],'%Y-%m-%d')

    # Create a movie here and append it to movies_in_db
    new_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(new_movie)

#Add movies to SQLAlchemy and then commit
model.db.session.add_all(movies_in_db)
model.db.session.commit()

#Create 10 users
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email, password)
    model.db.session.add(user)
    
    # Create 10 ratings for the user
    for x in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1,5)
        new_rating = crud.rate_a_movie(user, random_movie, score)
        model.db.session.add(new_rating)

model.db.session.commit()
    