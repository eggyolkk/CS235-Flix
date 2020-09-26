import pytest

from cs235flix.movies import services as movies_services
from cs235flix.movies.services import NonExistentMovieException


def test_can_get_movie(in_memory_repo):
    movie_rank = 2

    movie_as_dict = movies_services.get_movie(movie_rank, in_memory_repo)

    assert movie_as_dict['rank'] == movie_rank
    assert movie_as_dict['title'] == "Prometheus"
    assert movie_as_dict['date'] == "2012"
    assert movie_as_dict['description'] == "Following clues to the origin of mankind, a team finds a structure on a " \
                                           "distant moon, but they soon realize they are not alone."
    assert str(movie_as_dict['actors']) == "[<Actor Noomi Rapace>, <Actor Logan Marshall-Green>, <Actor Michael " \
                                      "Fassbender>, <Actor Charlize Theron>]"
    assert str(movie_as_dict['genres']) == "[<Genre Adventure>, <Genre Mystery>, <Genre Sci-Fi>]"
    assert str(movie_as_dict['director']) == "<Director Ridley Scott>"


def test_cannot_get_movie_with_non_existent_rank(in_memory_repo):
    movie_rank = 1001

    # Call the service layer to attempt to retrieve the Movie
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_rank, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movies_services.get_first_movie(in_memory_repo)

    # Note: Movies sorted in alphabetical order
    assert movie_as_dict['rank'] == 508


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movies_services.get_last_movie(in_memory_repo)

    # Note: Movies sorted in alphabetical order
    assert movie_as_dict['rank'] == 75


def test_get_movies_by_date_with_multiple_dates(in_memory_repo):
    target_date = 2009

    movies_as_dict, prev_date, next_date = movies_services.get_movies_by_date(target_date, in_memory_repo)

    assert len(movies_as_dict) == 51
    assert movies_as_dict[0]['rank'] == 508

    assert prev_date == 2008
    assert next_date == 2010


def test_get_movies_by_date_with_non_existent_date(in_memory_repo):
    target_date = 2022

    movies_as_dict, prev_date, next_date = movies_services.get_movies_by_date(target_date, in_memory_repo)

    # Check that there are no movies with the release date of 2022.
    assert len(movies_as_dict) == 0