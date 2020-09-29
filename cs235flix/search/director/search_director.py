from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import cs235flix.search.director.services as services
import cs235flix.adapters.repository as repo

# Configure Blueprint.
search_director_blueprint = Blueprint(
    'search_director_bp', __name__
)


@search_director_blueprint.route('/director', methods=['GET', 'POST'])
def director():
    form = SearchForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the input for director has passed the validation check.
        # Set the search to a variable.
        services.set_search(form.director.data, repo.repo_instance)

        # All is well, redirect user to results page.
        return redirect(url_for('search_director_bp.results'))

    # Request the display page
    return render_template(
        'search/search_page.html',
        title='Search results',
        search_variable="director",
        handler_url=url_for('search_director_bp.director'),
        form=form
    )


@search_director_blueprint.route('/director/results', methods=['GET'])
def results():
    movies_per_page = 5

    # Read query parameters
    cursor = request.args.get('cursor')

    search = services.get_search(repo.repo_instance)
    movies_list = services.search_director(search, repo.repo_instance)
    count = len(movies_list)
    plural = "movies"

    if count == 1:
        plural = "movie"

    if cursor is None:
        # No cursor query parameter so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)

    # Retrieve movie ranks for movies by director.
    movie_ranks = services.get_movie_ranks(movies_list, repo.repo_instance)

    # Retrieve the batch of movies to display on web page.
    movies = services.get_movies_by_type(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('search_director_bp.results', search=search, cursor=cursor - movies_per_page)
        first_movie_url = url_for('search_director_bp.results', search=search)

    if cursor + movies_per_page< len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('search_director_bp.results', search=search, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('search_actor_bp.results', search=search, cursor=last_cursor)

    return render_template(
        'movies/movies_by_search.html',
        movies=movies,
        name="by Director '" + str(search).capitalize() + "'",
        actor=str(search).capitalize(),
        count=count,
        movie_plural=plural,
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        next_movie_url=next_movie_url,
        prev_movie_url=prev_movie_url
    )


class SearchForm(FlaskForm):
    director = StringField('Search for Movies by Director', [
        DataRequired(message='Input required'),
        Length(min=3, message='Input too short')
    ])
    submit = SubmitField('Search')