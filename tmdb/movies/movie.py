from dataclasses import asdict, dataclass
from typing import Dict, List

from tmdb.casting.casting import Casting


@dataclass
class MovieDetails:
    id: int
    title: str
    original_title: str
    overview: str
    original_lang: str
    poster_img_path: str
    release_date: str
    genres: List[str]
    # actor_casting: List[Casting]
    external_ids: Dict[str, str]
    is_adult: bool

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.original_title = kwargs.get('original_title')
        self.overview = kwargs.get('overview')
        self.original_lang = kwargs.get('original_language')
        self.poster_img_path = kwargs.get('poster_path')
        self.release_date = kwargs.get('release_date')
        self.genres: List[str] = list(map(lambda genre: genre.get('name'),
                                          kwargs.get('genres')))
        # self.actor_casting = self.actors_only(casting=map(lambda movie: Casting(**movie),
        #                                                   kwargs.get('credits').get('cast')))
        self.external_ids = kwargs.get('external_ids')
        self.is_adult = kwargs.get('adult')

    def actors_only(self, casting) -> List[Casting]:
        return list(filter(lambda cast: cast.is_an_actor, casting))

    def to_bq(self) -> Dict:
        return asdict(self)
