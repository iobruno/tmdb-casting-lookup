import os
import requests as r
from typing import Dict

from tmdb.movies.movie import MovieDetails
from tmdb.utils.logger import get_logger

logger = get_logger("MovieApi")


class MovieApi:

    def __init__(self, bearer_token: str = os.environ['TMDB_API_KEY']):
        self.bearer_token = bearer_token
        self.movie_details_endpoint = "https://api.themoviedb.org/3/movie"

    def get_details(self, movie_id: int, language: str = "pt-br") -> MovieDetails:
        logger.info(f"Fetching Casting, Images and External IDs for movie id: '{movie_id}'")
        movie_details = r.get(f"{self.movie_details_endpoint}/{movie_id}",
                              params={'append_to_response': "credits,images,external_ids",
                                      'language': language},
                              headers={"Authorization": f"Bearer {self.bearer_token}"})

        raw_results: Dict[str, str] = movie_details.json()
        return MovieDetails(**raw_results)
