from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import cs235flix.adapters.repository as repo
import cs235flix.utilities.utilities as utilities
import cs235flix.movies.services as services


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/show_movies', methods=['GET'])
def show_movies():
    return render_template(
        'home/home.html',
        selected_movies=utilities.get_selected_movies()
    )