from typing import Iterable

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie


class NonExistentMovieException(Exception):
    pass


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movies(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'date': movie.release_date,
        'title': movie.title,
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
