from typing import List

import pytest
from cs235flix.domain.model import Movie
from cs235flix.adapters.repository import RepositoryException


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 1000 movies
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        "Testing",
        2020,
        1001,
        "Testing description",
        "Ron Clements",
        "Auli'i Cravalho, Dwayne Johnson, Rachel House, Temuera Morrison",
        "Animation,Adventure,Comedy"
    )
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(1001) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1001)
    assert movie is None


def test_repository_can_retrieve_movies_by_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(2009)

    # Check that the query returned 51 Movies.
    assert len(movies) == 51


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(2002)

    # Check that the query returned 0 Movies.
    assert len(movies) == 0


def test_repository_can_get_first_movie(in_memory_repo):
    # Check that the query returns the first movie in alphabetical order.
    movie = in_memory_repo.get_first_movie()
    assert movie.title == '(500) Days of Summer'


def test_repository_can_get_last_movie(in_memory_repo):
    # Check that the query returns the last movie in alphabetical order.
    movie = in_memory_repo.get_last_movie()
    assert movie.title == "Zootopia"


def test_repository_does_not_retrieve_movie_for_non_existent_rank(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([833, 1001])

    assert len(movies) == 1
    assert movies[
        0].title == 'Jane Eyre'


def test_repository_returns_an_empty_list_for_non_existent_ranks(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([0, 1001])

    assert len(movies) == 0


def test_repository_returns_date_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date == 2011


def test_repository_returns_none_when_there_are_no_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(79)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date is None


def test_repository_returns_date_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(93)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date == 2012


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(97)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date is None