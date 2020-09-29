from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie
from typing import Iterable


def set_search(search: str, repo: AbstractRepository):
    # Set the search to a variable in repo.
    repo.set_search(search)


def get_search(repo: AbstractRepository):
    # Retrieve the search user input
    search = repo.get_search()

    return search


def search_director(search: str, repo: AbstractRepository):
    # Get list of movies with director, if match found.
    movies = repo.get_movie_by_type(search, "director")

    return movies


def get_movie_ranks(movies: list, repo: AbstractRepository):
    rank_list = repo.get_movie_ranks_for_type(movies)

    return rank_list


def get_movies_by_type(rank_list: list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


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
