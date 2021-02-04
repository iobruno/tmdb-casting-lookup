from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TVShowDetails:
    tmdb_id: int
    imdb_id: str
    tvdb_id: Optional[str]
    title: str
    original_title: str
    overview: str
    original_lang: str
    genres: List[str]
    seasons: List['TVShowSeason']
    actor_casting: List['TVShowCast']
    is_adult: bool

    def __init__(self, **kwargs):
        self.tmdb_id = kwargs.get('id')
        self.imdb_id = kwargs.get('external_ids').get('imdb_id')
        self.tvdb_id = kwargs.get('external_ids').get('tvdb_id')
        self.title = kwargs.get('name')
        self.original_title = kwargs.get('original_name')
        self.overview = kwargs.get('overview')
        self.original_lang = kwargs.get('original_language')

        self.is_adult = kwargs.get('adult')
        self.genres: List[str] = list(map(lambda genre: genre.get('name'),
                                          kwargs.get('genres')))
        self.seasons: List[TVShowSeason] = list(map(lambda season: TVShowSeason(**season),
                                                    kwargs.get('seasons')))
        self.actor_casting = self.actors_only(casting=map(lambda casting: TVShowCast(**casting),
                                                          kwargs.get('credits').get('cast')))

    def actors_only(self, casting) -> List['TVShowCast']:
        return list(filter(lambda cast: cast.is_an_actor, casting))


@dataclass
class TVShowSeason:
    tmdb_id: int
    number: int
    name: str
    air_date: str
    num_episodes: int
    poster_img_path: str

    def __init__(self, **kwargs):
        self.tmdb_id = kwargs.get('id')
        self.number = kwargs.get('season_number')
        self.name = kwargs.get('name')
        self.air_date = kwargs.get('air_date')
        self.num_episodes = kwargs.get('episode_count')
        self.poster_img_path = kwargs.get('poster_path')

    @property
    def release_date(self):
        return self.air_date


@dataclass
class TVShowCast:
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
