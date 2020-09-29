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
        'movies/browse_movies.html',
        random=random_movie,
        title='Testing browse'
    )


"""@movies_blueprint.route('/browse_by_actor', methods=['GET'])
def browse_by_actor_index():
    # Generate the webpage to display the articles.
    return render_template(
        'movies/browse_by_actor_index.html',
        title='Testing browse by actor'
    )"""