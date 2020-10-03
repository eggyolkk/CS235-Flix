from datetime import date
import math

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import cs235flix.adapters.repository as repo
import cs235flix.utilities.utilities as utilities
import cs235flix.utilities.services as util_services
import cs235flix.movies.services as services

from cs235flix.authentication.authentication import login_required

# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/browse_movies', methods=['GET'])
def browse_movies():
    random_movie = util_services.get_random_movies(4, repo.repo_instance)
    return render_template(
        'movies/browse_movies.html',
        random=random_movie,
        page='random'
    )


@movies_blueprint.route('/movies_by_date', methods=['GET'])
def movies_by_date():
    movies_per_page = 10

    # Read query parameters.
    target_date = request.args.get('date')
    movie_to_show_reviews = request.args.get('view_reviews_for')
    cursor = request.args.get('cursor')
    starting_cursor = request.args.get('starting_cursor')
    max_cursor = request.args.get('max_cursor')
    prev_cursor = request.args.get('prev_cursor')

    # Set the starting cursor to be constant.
    starting_year_movies, previous_date2, next_date2 = services.get_movies_by_date(2006, repo.repo_instance)
    starting_ranks_len = len(starting_year_movies)
    starting_max_cursor = math.ceil(starting_ranks_len)

    current_max_cursor = starting_max_cursor

    if cursor is None or cursor == "0":
        # No cursor query parameter so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)

    if starting_cursor is not None:
        current_starting_cursor = int(starting_cursor)
    else:
        current_starting_cursor = 0

    if max_cursor is not None:
        current_max_cursor = int(max_cursor)

    if prev_cursor is not None:
        prev_cursor = int(prev_cursor)

    # Fetch the first and last movies in the series
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_date is None:
        # No date query parameter, so return movies from earliest movie release date.
        target_date = first_movie['year']
    else:
        # Convert target_date from string to int.
        target_date = int(target_date)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) for the target date. This call also returns the previous and next dates for movies immediately
    # before and after the target date.
    movies, previous_date, next_date = services.get_movies_by_date(target_date, repo.repo_instance)

    # Retrieve movie ranks for movies released in that year.
    movie_ranks = services.get_movie_ranks(movies, repo.repo_instance)

    # Retrieve the batch of movies to display on web page,
    movie_batch = services.get_movies_by_type(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    movie_ranks_len = len(movie_ranks)

    # Get previous max cursor and previous cursor
    if previous_date is not None:
        prev_movies, prev_previous_date, prev_next_date = services.get_movies_by_date(int(target_date)-1, repo.repo_instance)
        prev_max_cursor = math.ceil(len(prev_movies))
        extra = int(len(prev_movies)) % 10
        prev_cursor = int(len(prev_movies)) - extra

    # Get last max cursor and cursor
    last_movies, last_previous_date, last_next_date = services.get_movies_by_date(int(last_movie['year']), repo.repo_instance)
    extra = int(len(last_movies)) % 10
    last_max_cursor = math.ceil(len(last_movies))
    last_cursor = int(len(last_movies)) - extra

    if len(movies) > 0:
        # Generate the URL for the first navigation button for all pages except the first.
        if previous_date is not None or (cursor > 0 and previous_date is None):
            first_movie_url = url_for('movies_bp.movies_by_date', date=first_movie['year'])

        # Generate the URL for the next navigation button for the earliest date.
        if previous_date is None:
            next_movie_url = url_for('movies_bp.movies_by_date', date=target_date, cursor=cursor + movies_per_page, starting_cursor=0, max_cursor=current_max_cursor)
            if cursor > 0:
                prev_movie_url = url_for('movies_bp.movies_by_date', date=target_date, cursor=cursor - movies_per_page)
        else:
            # There are movies on previous dates.
            # Navigate previous movies for the PREVIOUS year.
            if cursor == 0:
                prev_movie_url = url_for('movies_bp.movies_by_date', date=previous_date, cursor=prev_cursor, max_cursor=prev_max_cursor)
            elif cursor > 0:
                # Navigate previous movies within the SAME year.
                prev_movie_url = url_for('movies_bp.movies_by_date', date=target_date, cursor=cursor - movies_per_page, max_cursor=current_max_cursor)

        # There are movies on subsequent dates.
        if next_date is not None:
            # Navigate next movies for the NEXT year.
            if cursor + movies_per_page > current_max_cursor:
                next_movie_url = url_for('movies_bp.movies_by_date', date=next_date, cursor=0, starting_cursor=starting_cursor, max_cursor=math.ceil(movie_ranks_len))
            else:
                # Navigate next movies within the SAME year.
                next_movie_url = url_for('movies_bp.movies_by_date', date=target_date, cursor=cursor + movies_per_page, max_cursor=current_max_cursor)
        else:
            if cursor + movies_per_page < current_max_cursor:
                # Navigate next movies within the SAME year.
                next_movie_url = url_for('movies_bp.movies_by_date', date=target_date, cursor=cursor + movies_per_page, max_cursor=current_max_cursor)

        # Generate the URL for the last navigation button for all pages except the last.
        if next_date is None and (cursor + movies_per_page <= math.ceil(movie_ranks_len)) or next_date is not None:
            last_movie_url = url_for('movies_bp.movies_by_date', date=last_movie['year'], cursor=last_cursor, starting_cursor=0, max_cursor=last_max_cursor)

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movie_batch:
            movie['view_review_url'] = url_for('movies_bp.movies_by_date', date=target_date, view_reviews_for=movie['rank'])
            movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])
            movie['add_to_watchlist_url'] = url_for('watchlist_bp.add_to_watchlist', movie=movie['rank'])

    # Generate the webpage to display the movies.
    return render_template(
        'movies/browse_movies.html',
        title='Movies',
        movies_title=target_date,
        movies=movie_batch,
        selected_movies=utilities.get_selected_movies(len(movies)*2),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movies=movie_to_show_reviews,
        page='year'
        )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with a movie rank, when subsequently called with a HTTP POST request, the movie rank remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie rank, representing the reviewed movie, from the form.
        movie_rank = int(form.movie_rank.data)
        get_search = form.search_data.data
        get_search_cursor = int(form.search_cursor_data.data)
        get_search_page = form.search_page_data.data
        get_search_type = form.search_type.data

        # Use the service layer to store the new review.
        services.add_review(movie_rank, form.review.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_rank, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same date as the reviewed movie,
        # and display all reviews, including the new review.
        if get_search_type == "actor" or get_search_type == "director" or get_search_type == "genres" or get_search_type == "movie":
            return redirect(
                url_for('search_bp.results', search=get_search, cursor=get_search_cursor, view_reviews_for=movie_rank,
                        search_type=get_search_type))
        else:
            return redirect(url_for('movies_bp.movies_by_date', date=movie['year'], view_reviews_for=movie_rank))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie rank, representing the movie to review, from a query parameter of the GET request.
        movie_rank = int(request.args.get('movie'))
        search_page = request.args.get('search_page')
        search = request.args.get('search')
        search_cursor = int(request.args.get('search_cursor'))
        search_type = request.args.get('search_type')

        # Store the movie rank in the form.
        form.movie_rank.data = movie_rank
        form.search_data.data = search
        form.search_page_data.data = search_page
        form.search_cursor_data.data = search_cursor
        form.search_type.data = search_type


    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie rank of the movie being reviewed from the form.
        movie_rank = int(form.movie_rank.data)
        search_page = str(form.search_page_data.data)
        search = str(form.search_data.data)
        search_cursor = form.search_cursor_data.data

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_rank, repo.repo_instance)
    return render_template(
        'movies/review_on_movie.html',
        title='Edit movie',
        movie=movie,
        rank=movie_rank,
        form=form,
        handler_url=url_for('movies_bp.review_on_movie'),
        selected_movies=utilities.get_selected_movies(),
        page="search"
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = 'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short.'),
        ProfanityFree(message='Your review must not contain profanity')])

    movie_rank = HiddenField("Movie rank")
    search_data = HiddenField("Search")
    search_page_data = HiddenField("Search page")
    search_cursor_data = HiddenField("Search cursor")
    search_type = HiddenField("Search type")
    submit = SubmitField("Submit")
