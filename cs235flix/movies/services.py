from typing import Iterable

import cs235flix.adapters.repository as repo
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie


class NonExistentMovieException(Exception):
    pass


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_date(date, repo: AbstractRepository):
    # Returns movies for the target date (empty if no matches), the date of the previous movie (might be null), the date
    # of the next movie (might be null)

    movies = repo.get_movies_by_date(target_date=date)
    print("test")
    movies_dto = list()
    prev_date = next_date = None

    if len(movies) > 0:
        prev_date = repo.get_date_of_previous_movie(movies[0])
        next_date = repo.get_date_of_next_movie(movies[0])

        # Convert Movies to dictionary form
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_date, next_date


def get_movies_by_actor(initials, repo: AbstractRepository):
    # Returns movies which include actors with their first letter specified by variable initials.

    movies = repo.get_movie_by_actor(initials)

    return movies


def get_movie_ranks_for_actor(movies: list, repo: AbstractRepository):
    # Returns a list of ranks for the movies with starring actors.

    rank_list = repo.get_movie_ranks_for_actor(movies)

    return rank_list

# ============================================
# Functions to convert model entities to dicts
# ============================================


def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'date': movie.release_date,
        'title': movie.title,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'genres': movie.genres
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
