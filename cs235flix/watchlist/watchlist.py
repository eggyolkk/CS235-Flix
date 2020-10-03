from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask import jsonify

import cs235flix.adapters.repository as repo
import cs235flix.utilities.utilities as utilities
import cs235flix.utilities.services as util_services
import cs235flix.watchlist.services as services

from cs235flix.authentication.authentication import login_required

# Configure Blueprint.
watchlist_blueprint = Blueprint(
    'watchlist_bp', __name__)


@watchlist_blueprint.route('/watchlist', methods=['GET'])
# @login_required
def watchlist():
    return render_template(
        'watchlist/watchlist.html',
        title='Watchlist',
        test_script="shigatsu"
    )


@watchlist_blueprint.route('/add_to_watchlist', methods=['GET'])
@login_required
def add_to_watchlist():
    # Obtain the username of the currently logged in user.
    username = session['username']

    movie_rank = int(request.args.get('movie'))

    return render_template(
        'watchlist/watchlist.html',
        title='Added to watchlist',
        movie_rank=movie_rank
    )