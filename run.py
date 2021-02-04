import click
from typing import List, Dict

from app.search.search_api import SearchApi, SearchResult
from app.movies.movie_api import MovieApi
from app.tv.tv_show_api import TvShowApi


@click.command()
@click.option("-q", "--query", required=True, type=str,
              help="Query for the movie or tv show.")
def run(query):
    search_results: Dict[str, List[SearchResult]] = SearchApi().query(query_string=query)
    movies = search_results.get('movie', [])
    tv_shows = search_results.get('tv', [])

    movie_api, tv_api = MovieApi(), TvShowApi()
    movie_details = map(lambda movie: movie_api.get_details(movie.id), movies)
    tv_show_details = map(lambda tv_show: tv_api.get_details(tv_show.id), tv_shows)


if __name__ == "__main__":
    run()
