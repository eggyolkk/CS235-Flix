import pytest

from flask import session


def test_browse_movies(client):
    # Check that we can retrieve the movies page.
    response = client.get('/browse_movies')
    assert response.status_code == 200

