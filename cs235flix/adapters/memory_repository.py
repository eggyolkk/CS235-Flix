import csv
import os
from typing import List

from bisect import bisect_left, insort_left

from cs235flix.adapters.repository import AbstractRepository, RepositoryException
from cs235flix.domain.model import Actor, Genre, Director, Movie


class MemoryRepository(AbstractRepository):
    # Movies ordered by name.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()

    @property
    def get_index(self):
        return self._movies_index

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.rank] = movie

    def get_movie(self, rank: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[rank]
        except KeyError:
            # Ignore exception and return None
            pass

        return movie

    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        matching_movies = list()

        for movie in self._movies:
            if int(movie.release_date) == target_date:
                matching_movies.append(movie)
        if len(matching_movies) == 0:
            return []
        else:
            return matching_movies

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_movies_by_rank(self, rank_list):
        # Strip out any ids in id_list that don't represent Movie ids in the repository.
        existing_ranks = [rank for rank in rank_list if rank in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[rank] for rank in existing_ranks]
        return movies

    def get_date_of_previous_movie(self, movie: Movie):
        previous_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.release_date < movie.release_date:
                    previous_date = stored_movie.release_date
                    break
        except ValueError:
            # No earlier movies, so return None
            pass

        return previous_date

    def get_date_of_next_movie(self, movie: Movie):
        next_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.release_date > movie.release_date:
                    next_date = stored_movie.release_date
                    break
        except ValueError:
            # No subsequent movies, so return None.
            pass

        return next_date

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_date == movie.release_date:
            return index
        raise ValueError


class MovieFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self._dataset_of_movies = []
        self._dataset_of_actors = []
        self._dataset_of_directors = []
        self._dataset_of_genres = []
        self._dataset_of_descriptions = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                add_rank = row['Rank']
                add_title = row['Title']
                add_year = int(row['Year'])
                add_description = row['Description']
                add_movie = Movie(add_title, add_year, add_rank, add_description)
                self._dataset_of_movies.append(add_movie)

                actors_list = row['Actors'].split(",")
                for a in actors_list:
                    actor = a.strip()
                    add_actor = Actor(actor)
                    if add_actor not in self._dataset_of_actors:
                        self._dataset_of_actors.append(add_actor)

                directors_list = row['Director'].split(",")
                for d in directors_list:
                    add_director = Director(d)
                    if add_director not in self._dataset_of_directors:
                        self._dataset_of_directors.append(add_director)

                genre_list = row['Genre'].split(",")
                for g in genre_list:
                    add_genre = Genre(g)
                    if add_genre not in self._dataset_of_genres:
                        self._dataset_of_genres.append(add_genre)

                index += 1

    @property
    def dataset_of_movies(self):
        return self._dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self._dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self._dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self._dataset_of_genres


def load_movies(data_path: str, repo: MemoryRepository):
    movie_file_reader = MovieFileCSVReader(os.path.join(data_path))
    movie_file_reader.read_csv_file()

    for movie in movie_file_reader.dataset_of_movies:
        repo.add_movie(movie)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies into the repository
    load_movies(data_path, repo)


"""new_repo = MemoryRepository()
c_path = os.path.abspath("data/Data1000Movies.csv")
guardians = Movie("Guardians of the Galaxy", 2014, 1)

populate(c_path, new_repo)
print("First movie", new_repo.get_first_movie())
print(new_repo.get_movies_by_date(2009))"""