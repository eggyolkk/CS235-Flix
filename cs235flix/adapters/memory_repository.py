from cs235flix.adapters.data.repository import AbstractRepository
from cs235flix.domain.model import Movie


class MemoryRepository(AbstractRepository):
    #Movies ordered by name.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._tags = list()

    def add_movie(self, movie: Movie):
        self._movies.append(movie)

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[id]
        except KeyError:
            pass # Ignore exception and return None

        return movie


""" def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Movie ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def get_movies_ids_for_tag(self, tag_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        tag = next((tag for tag in self._tags if tag.tag_name == tag_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if tag is not None:
            movies_ids = [movie.id for movie in tag.tagged_movies]
        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        return movie_ids"""