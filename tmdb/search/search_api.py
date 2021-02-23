import requests as r
from itertools import groupby
from operator import attrgetter
from typing import Dict, List

from tmdb.search.search_results import SearchResult


class SearchApi:

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.search_endpoint = "https://api.themoviedb.org/3/search/multi"

    def query(self, query_string: str, language: str = "pt-br") -> Dict[str, List[SearchResult]]:
        """
        :param language: specifies the language for which the 'title' and 'overview'
                         will be displayed at
        :param query_string: search by the 'movie title', 'tv show title' or 'celebrity name'
        :return: a Dictionary might contain up to 3 keys 'movie', 'tv', and 'person'
                 each key containing the list of matches for their respective key
        """
        multi_search = r.get(self.search_endpoint,
                             params={'query': query_string, 'language': language},
                             headers={"Authorization": f"Bearer {self.bearer_token}"})
        raw_results: List[Dict[str, str]] = multi_search.json().get('results')
        search_results: List[SearchResult] = self._parse(search_results=raw_results)
        grp_search_results = {key: list(val)
                              for key, val in groupby(search_results, attrgetter('media_type'))}

        return grp_search_results

    # TODO: to be implemented
    def discover(self):
        NotImplemented("Not yet implemented")

    def _parse(self,
               search_results: List[Dict[str, str]],
               sort_key: str = 'popularity') -> List[SearchResult]:
        results = sorted(search_results, reverse=True, key=lambda result: result.get(sort_key))
        return [SearchResult(**entry) for entry in results]
