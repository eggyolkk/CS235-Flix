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
        self._search = ""

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
        # Strip out any ranks in rank_list that don't represent Movie ranks in the repository.
        existing_ranks = [rank for rank in rank_list if rank in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[rank] for rank in existing_ranks]
        return movies

    def get_date_of_previous_movie(self, movie: Movie):
        previous_date = None
        current_date = 0

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies):
                if int(movie.release_date) > int(stored_movie.release_date) > int(current_date):
                    previous_date = stored_movie.release_date
                    current_date = stored_movie.release_date
        except ValueError:
            # No earlier movies, so return None
            pass

        if previous_date is not None:
            return int(previous_date)
        return previous_date

    def get_date_of_next_movie(self, movie: Movie):
        next_date = None
        current_date = 2020

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies:
                if int(current_date) > int(stored_movie.release_date) > int(movie.release_date):
                    current_date = stored_movie.release_date

                if int(movie.release_date) < int(stored_movie.release_date) <= int(current_date):
                    next_date = stored_movie.release_date
        except ValueError:
            # No subsequent movies, so return None.
            pass

        if next_date is not None:
            return int(next_date)
        return next_date

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_date == movie.release_date:
            return index
        raise ValueError

    def get_movie_ranks_for_actor(self, movies: list):
        rank_list = []

        for movie in movies:
            rank_list.append(int(movie.rank))

        return rank_list

    def get_movie_by_actor(self, search: str):
        movies_with_actor = []
        search = search.lower()

        for movie in self._movies:
            for actor in movie.actors:
                if search in str(actor).lower():
                    movies_with_actor.append(movie)

        return movies_with_actor

    def set_search(self, search: str):
        self._search = search


    def get_search(self):
        return self._search


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
                add_actors = []
                add_genres = []
                add_director = ""

                actors_list = row['Actors'].split(",")
                for a in actors_list:
                    actor = a.strip()
                    add_actor = Actor(actor)
                    if add_actor not in self._dataset_of_actors:
                        self._dataset_of_actors.append(add_actor)
                    add_actors.append(add_actor)

                directors_list = row['Director'].split(",")
                for d in directors_list:
                    add_director = Director(d)
                    if add_director not in self._dataset_of_directors:
                        self._dataset_of_directors.append(add_director)
                    add_director = d

                genre_list = row['Genre'].split(",")
                for g in genre_list:
                    add_genre = Genre(g)
                    if add_genre not in self._dataset_of_genres:
                        self._dataset_of_genres.append(add_genre)
                    add_genres.append(add_genre)

                add_movie = Movie(add_title, add_year, add_rank, add_description, add_director, add_actors, add_genres)
                self._dataset_of_movies.append(add_movie)

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

populate(c_path, new_repo)
movies = new_repo.get_movie_by_actor("z")
print(new_repo.get_movie_ranks_for_actor(movies))"""