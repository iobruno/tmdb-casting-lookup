from dataclasses import dataclass
from typing import List


@dataclass
class MovieDetails:
    tmdb_id: int
    imdb: str
    title: str
    original_title: str
    overview: str
    original_lang: str
    release_date: str
    genres: List[str]
    actor_casting: List['MovieCast']
    is_adult: bool

    def __init__(self, **kwargs):
        """media_type is either 'movie' or 'tv' """
        self.tmdb_id = kwargs.get('id')
        self.imdb_id = kwargs.get('imdb_id')
        self.title = kwargs.get('title')
        self.original_title = kwargs.get('original_title')
        self.overview = kwargs.get('overview')
        self.original_lang = kwargs.get('original_language')
        self.release_date = kwargs.get('release_date')
        self.is_adult = kwargs.get('adult')
        self.genres: List[str] = list(map(lambda genre: genre.get('name'),
                                          kwargs.get('genres')))
        self.actor_casting = self.actors_only(casting=map(lambda movie: MovieCast(**movie),
                                                          kwargs.get('credits').get('cast')))

    def actors_only(self, casting) -> List['MovieCast']:
        return list(filter(lambda cast: cast.is_an_actor, casting))


@dataclass
class MovieCast:
    id: int
    name: str
    original_name: str
    character: str
    gender: int
    department: str

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.original_name = kwargs.get('original_name')
        self.character = kwargs.get('character')
        self.profile_img_id = kwargs.get('profile_path')
        self.gender = kwargs.get('gender')
        self.department = kwargs.get('known_for_department')

    @property
    def is_an_actor(self) -> bool:
        return self.department == 'Acting'

    @property
    def is_female(self) -> bool:
        return self.gender == 1

    @property
    def is_male(self) -> bool:
        return not self.is_female
