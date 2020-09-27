from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import cs235flix.adapters.repository as repo
import cs235flix.utilities.utilities as utilities
import cs235flix.utilities.services as util_services
import cs235flix.movies.services as services


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/browse_movies', methods=['GET'])
def browse_movies():
    random_movie = util_services.get_random_movies(4, repo.repo_instance)
    return render_template(
        'movies/movies.html',
        random=random_movie,
        title='Testing browse'
    )


@movies_blueprint.route('/browse_by_actor', methods=['GET'])
def browse_by_actor_index():
    # Generate the webpage to display the articles.
    return render_template(
        'movies/browse_by_actor_index.html',
        title='Testing browse by actor'
    )


@movies_blueprint.route('/browse_by_actor', methods=['GET'])
def browse_by_actor():
    movies_per_page = 4

    # Read query parameters.
    # initials = request.args.get('initials')
    initials = "a"
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Fetch movies with starring actors.
    movies_with_actor = services.get_movies_by_actor(initials, repo.repo_instance)

    # Retrieve movie ranks for movies with starring actors.
    movie_ranks = services.get_movie_ranks_for_actor(movies_with_actor, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.browse_by_actor', initials=initials, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.browse_by_actor', initials=initials)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.browse_by_actor', initials=initials, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.browse_by_actor', initials=initials, cursor=last_cursor)

    # Generate the webpage to display the articles.
    return render_template(
    )


"""@movies_blueprint.route('/movies_by_date', methods=['GET'])
def movies_by_date():
    # Read query parameters.
    target_date = request.args.get('date')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_date is None:
        # No date query parameter, so return articles from day 1 of the series.
        target_date = first_movie['date']
    else:
        # Convert target_date from string to date.
        target_date = int(target_date)

    # Fetch movie(s) for the target date. This call also returns the previous and next dates for articles immediately
    # before and after the target date.
    movies, previous_date, next_date = services.get_movies_by_date(target_date, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    movie_type=type(first_movie)

    if len(movies) > 0:
        # There's at least one movie for the target date.
        if previous_date is not None:
            # There are movies on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_date', date=previous_date)
            first_movie_url = url_for('movies_bp.movies_by_date', date=first_movie['date'])

        # There are movies on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_date is not None:
            next_movie_url = url_for('movies_bp.articles_by_date', date=next_date.isoformat())
            last_movie_url = url_for('movies_bp.articles_by_date', date=last_movie['date'].isoformat())

        # Generate the webpage to display the movies
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url
        )
    else:
        return render_template(
            'movies/movies.html',
            title='No movies',
            first_movie=last_movie,
            type=movie_type
        )"""