from dataclasses import dataclass
from typing import Dict, List, Optional

from tmdb.casting.casting import Casting


@dataclass
class TVShowDetails:
    id: int
    title: str
    original_title: str
    overview: str
    original_lang: str
    poster_img_path: str
    genres: List[str]
    seasons: List['TVShowSeason']
    actor_casting: List[Casting]
    external_ids: Dict[str, str]

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('name')
        self.original_title = kwargs.get('original_name')
        self.overview = kwargs.get('overview')
        self.original_lang = kwargs.get('original_language')
        self.poster_img_path = kwargs.get('poster_path')
        self.genres: List[str] = list(map(lambda genre: genre.get('name'),
                                          kwargs.get('genres')))
        self.seasons: List[TVShowSeason] = list(map(lambda season: TVShowSeason(**season),
                                                    kwargs.get('seasons')))
        self.actor_casting = self.actors_only(casting=map(lambda casting: Casting(**casting),
                                                          kwargs.get('credits').get('cast')))
        self.external_ids = kwargs.get('external_ids')

    def actors_only(self, casting) -> List[Casting]:
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