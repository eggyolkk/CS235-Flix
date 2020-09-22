class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name: str = actor_full_name.strip()
        self._actor_colleagues: list = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self) -> str:
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return other.__actor_full_name == self.__actor_full_name

    def __lt__(self, other) -> bool:
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self) -> str:
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        self._actor_colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague) -> bool:
        return colleague in self._actor_colleagues

class Genre:
    def __init__(
            self, genre_name: str
    ):
        if genre_name == "":
            self._genre_name: str = "None"
        else:
            self._genre_name: str = genre_name

    @property
    def genre_name(self) -> str:
        return self._genre_name

    def __repr__(self) -> str:
        return f'<Genre {self._genre_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Genre):
            return False
        return other._genre_name == self._genre_name

    def __lt__(self, other) -> bool:
        return self._genre_name < other._genre_name

    def __hash__(self) -> str:
        return hash(self._genre_name)

class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name: str = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self) -> str:
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Director):
            return False
        return other.director_full_name == self.__director_full_name

    def __lt__(self, other) -> bool:
        return self.__director_full_name < other.director_full_name

    def __hash__(self) -> str:
        return hash(self._director_full_name)

class Movie:
    def __init__(self, movie_title: str, release_date: int):
        if movie_title == "" or type(movie_title) is not str:
            self.__movie_title = None
        else:
            self.__movie_title: str = movie_title.strip()

        self.__release_date: int = release_date
        self.__description: str = None
        self.__director: Director = Director("")
        self.__actors: list = []
        self.__genres: list = []
        self.__runtime_minutes: int = None


    @property
    def title(self) -> str:
        return str(self.__movie_title)

    @property
    def release_date(self) -> int:
        return str(self.__release_date)

    @property
    def description(self) -> str:
        return str(self.__description)

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self) -> list:
        return self.__actors

    @property
    def genres(self) -> list:
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @title.setter
    def title(self, title):
        self.__title = title

    @release_date.setter
    def release_date(self, release_date):
        if release_date >= 1900:
            self.__release_date = release_date

    @description.setter
    def description(self, description):
        self.__description = description.strip()

    @director.setter
    def director(self, director):
        self.__director = director

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if runtime_minutes > 0:
            self.__runtime_minutes = runtime_minutes
        else:
            raise ValueError

    def __repr__(self) -> str:
        reprstring = "<Movie " + self.__movie_title + ", " + str(self.__release_date) + ">"
        return reprstring

    def __eq__(self, other) -> bool:
        if self.title == other.title and self.__release_date == other.release_date:
            return True
        else:
            return False

    def __lt__(self, other) -> bool:
        if self.title < other.title:
            return True
        elif self.title == other.title and self.__release_date < other.release_date:
            return True
        else:
            return False

    def __hash__(self) -> str:
        unique_movie = str(self.__movie_title) + str(self.__release_date)
        return hash(unique_movie)

    def add_actor(self, actor):
        if actor not in self.__actors:
            self.__actors.append(actor)

    def remove_actor(self, actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre):
        if genre not in self.__genres:
            self.__genres.append(genre)

    def remove_genre(self, genre):
        if genre in self.__genres:
            self.__genres.remove(genre)