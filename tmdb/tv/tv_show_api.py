import requests as r
from typing import Dict

from tmdb.tv.tv_show import TVShowDetails
from tmdb.utils.logger import get_logger

logger = get_logger("TvShowApi")


class TvShowApi:

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.movie_details_endpoint = "https://api.themoviedb.org/3/tv"

    def get_details(self, tv_show_id: int, language: str = "pt-br") -> TVShowDetails:
        logger.info(f"Fetching Casting, Images and External IDs for TV Show id: '{tv_show_id}'")
        tv_show_details = r.get(f"{self.movie_details_endpoint}/{tv_show_id}",
                                params={'append_to_response': "credits,images,external_ids",
                                        'language': language},
                                headers={"Authorization": f"Bearer {self.bearer_token}"})

        raw_results: Dict[str, str] = tv_show_details.json()
        return TVShowDetails(**raw_results)
