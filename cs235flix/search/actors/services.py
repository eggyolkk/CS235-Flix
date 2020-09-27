from cs235flix.adapters.repository import AbstractRepository


def set_search(search: str, repo: AbstractRepository):
    # Set the search to a variable in repo.
    repo.set_search(search)


def get_search(repo: AbstractRepository):
    # Retrieve the search user input
    search = repo.get_search()

    return search


def search_actor(search: str, repo: AbstractRepository):
    # Get list of movies with starring actor, if match found.
    movies = repo.get_movie_by_actor(search)

    return movies
