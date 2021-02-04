import os
import requests as r
from typing import Dict

from app.tv.tv_show import TVShowDetails


class TvShowApi:

    def __init__(self, bearer_token: str = os.environ['TMDB_API_KEY']):
        self.bearer_token = bearer_token
        self.movie_details_endpoint = "https://api.themoviedb.org/3/tv"

    def get_details(self, tv_show_id: int, language: str = "pt-br") -> TVShowDetails:
        tv_show_details = r.get(f"{self.movie_details_endpoint}/{tv_show_id}",
                                params={'append_to_response': "credits,images,external_ids",
                                        'language': language},
                                headers={"Authorization": f"Bearer {self.bearer_token}"})

        raw_results: Dict[str, str] = tv_show_details.json()
        return TVShowDetails(**raw_results)
