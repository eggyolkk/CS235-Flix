from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from functools import wraps

import cs235flix.utilities.utilities as utilities
import cs235flix.search.actors.services as services
import cs235flix.adapters.repository as repo

# Configure Blueprint.
search_actor_blueprint = Blueprint(
    'search_actor_bp', __name__
)


@search_actor_blueprint.route('/actor', methods=['GET', 'POST'])
def actor():
    form = SearchForm()

    typed = type(form.actor.data)

    if form.validate_on_submit():
        # Successful POST, i.e. the input for actor has passed the validation check.
        # Set the search to a variable.
        services.set_search(form.actor.data, repo.repo_instance)

        # All is well, redirect user to results page.
        return redirect(url_for('search_actor_bp.results'))


    # Request the display page
    return render_template(
        'search/search_actor.html',
        title='Search results',
        handler_url=url_for('search_actor_bp.actor'),
        type=typed,
        form=form
    )


@search_actor_blueprint.route('/actor/results', methods=['GET'])
def results():
    search = services.get_search(repo.repo_instance)
    movies = services.search_actor(search, repo.repo_instance)

    return render_template(
        'movies/movies.html',
        title='Search results success'
    )


class SearchForm(FlaskForm):
    actor = StringField('Actor', [
        DataRequired(message='Input required'),
        Length(min=3, message='Input too short')
    ])
    submit = SubmitField('Search')