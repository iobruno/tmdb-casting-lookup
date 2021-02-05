from typing import Dict, List

import typer

from tmdb.movies.movie_api import MovieApi
from tmdb.search.search_api import SearchApi, SearchResult
from tmdb.tv.tv_show_api import TvShowApi

app = typer.Typer()


@app.command("discover")
def discover_and_fetch():
    NotImplemented("Discover is not yet implemented")


@app.command("search")
def search_and_fetch(query: str = typer.Option(..., "-q", "--query",
                                               help="Query movies, tv shows by name")):
    search_results: Dict[str, List[SearchResult]] = SearchApi().query(query_string=query)
    movies = search_results.get('movie', [])
    tv_shows = search_results.get('tv', [])

    movie_api, tv_api = MovieApi(), TvShowApi()
    movie_details = map(lambda movie: movie_api.get_details(movie.id), movies)
    tv_show_details = map(lambda tv_show: tv_api.get_details(tv_show.id), tv_shows)


def run():
    app()
