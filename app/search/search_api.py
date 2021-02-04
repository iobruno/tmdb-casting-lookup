import os
from typing import Dict, List

import requests as r

from app.search.search_results import SearchResult


class SearchApi:

    def __init__(self, bearer_token: str = os.environ['TMDB_API_KEY']):
        self.bearer_token = bearer_token
        self.search_endpoint = "https://api.themoviedb.org/3/search/multi"

    def query(self, query_string: str, language: str = "pt-br") -> List[SearchResult]:
        multi_search = r.get(self.search_endpoint,
                             params={'query': query_string, 'language': language},
                             headers={"Authorization": f"Bearer {self.bearer_token}"})
        raw_results: List[Dict[str, str]] = multi_search.json().get('results')
        search_results: List[SearchResult] = self._parse(search_results=raw_results)
        return search_results

    def _parse(self,
               search_results: List[Dict[str, str]],
               sort_key: str = 'popularity') -> List[SearchResult]:
        results = sorted(search_results, reverse=True, key=lambda result: result.get(sort_key))
        sorted_results = [SearchResult(**entry) for entry in results]
        return sorted_results
