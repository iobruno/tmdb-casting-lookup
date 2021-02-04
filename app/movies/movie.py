from dataclasses import dataclass
from typing import List

from app.casting.casting import Casting


@dataclass
class MovieDetails:
    tmdb_id: int
    imdb_id: str
    title: str
    original_title: str
    overview: str
    original_lang: str
    release_date: str
    genres: List[str]
    actor_casting: List[Casting]
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
        self.actor_casting = self.actors_only(casting=map(lambda movie: Casting(**movie),
                                                          kwargs.get('credits').get('cast')))

    def actors_only(self, casting) -> List[Casting]:
        return list(filter(lambda cast: cast.is_an_actor, casting))
