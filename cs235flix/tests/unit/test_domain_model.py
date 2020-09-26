from cs235flix.domain.model import Actor, Genre, Director, Movie

import pytest


@pytest.fixture()
def movie():
    return Movie(
        "Moana",
        2016,
        14,
        "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the Demigod to set things right.",
        "Ron Clements",
        "Auli'i Cravalho, Dwayne Johnson, Rachel House, Temuera Morrison",
        "Animation,Adventure,Comedy"
    )


def test_movie_construction(movie):
    assert movie.title == "Moana"
    assert movie.rank == 14
    assert movie.release_date == "2016"
    assert movie.description == "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the Demigod to set things right."
    assert movie.actors == "Auli'i Cravalho, Dwayne Johnson, Rachel House, Temuera Morrison"
    assert str(movie.director) == "<Director Ron Clements>"
    assert movie.genres == "Animation,Adventure,Comedy"


def test_movie_less_than_operator(movie):
    movie_1 = movie
    movie_2 = Movie(
        "Inglourious Basterds",
        2009,
        78,
        "Quentin Tarantino",
        "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans for the same.",
        "Brad Pitt, Diane Kruger, Eli Roth,Mélanie Laurent",
        "Adventure,Drama,War"
    )

    assert movie_2 <movie_1
