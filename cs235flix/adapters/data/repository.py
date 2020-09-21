from cs235flix.domain.model import Actor, Genre, Director, Movie


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_movies(self, id: int) -> Movie:
        """ Returns Movie with id from the repository.

         If there is no Movie with the given id, this method returns None.
         """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        """ Returns a list of Movies, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Movies that are tagged by genre_name.

        If there are Movies that are tagged by genre_name, this method returns an empty list.
        """
        raise NotImplementedError