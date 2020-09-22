import csv
import os

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie


class MemoryRepository(AbstractRepository):
    # Movies ordered by name.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()

    def add_movie(self, movie: Movie):
        self._movies.append(movie)

    def get_movies(self, rank: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[rank]
        except KeyError:
            pass # Ignore exception and return None

        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_movies_by_rank(self, rank_list):
        # Strip out any ids in id_list that don't represent Movie ids in the repository.
        existing_ranks = [rank for rank in rank_list if rank in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[rank] for rank in existing_ranks]
        return movies


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies(data_path: str, repo: MemoryRepository):
    for data_row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        # Create Movie object.
        movie = Movie(
            movie_title=data_row[1],
            release_date=int(data_row[6])
        )

        # Add the Movie to the repository.
        repo.add_movie(movie)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies into the repository
    load_movies(data_path, repo)