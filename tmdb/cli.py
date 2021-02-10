from typing import Dict, List

import apache_beam as beam
import typer
from apache_beam.io import BigQueryDisposition as BQDisposition

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

    with beam.Pipeline() as pipeline:
        movies = (pipeline
                  | 'Create Movies' >> beam.Create(movies)
                  | beam.Map(lambda movie: movie_api.get_details(movie.id).to_bq()))

        tv_shows = (pipeline
                    | 'Create TV Shows' >> beam.Create(tv_shows)
                    | beam.Map(lambda tv_show: tv_api.get_details(tv_show.id).to_bq()))

        movies | 'Movies to BQ' >> beam.io.WriteToBigQuery("recomendacao-gcom:reglobinition.casting_movies",
                                                           schema=fetch_movies_schema(),
                                                           write_disposition=BQDisposition.WRITE_APPEND,
                                                           create_disposition=BQDisposition.CREATE_IF_NEEDED,
                                                           custom_gcs_temp_location="gs://recomendacao-reglobinition/")

        tv_shows | 'TV Shows to BQ' >> beam.io.WriteToBigQuery("recomendacao-gcom:reglobinition.casting_tv",
                                                               schema=fetch_tv_shows_schema(),
                                                               write_disposition=BQDisposition.WRITE_APPEND,
                                                               create_disposition=BQDisposition.CREATE_IF_NEEDED,
                                                               custom_gcs_temp_location="gs://recomendacao-reglobinition/")


def fetch_tv_shows_schema() -> Dict:
    return {'fields': [
        {'name': "id", 'type': "INT64", 'mode': "REQUIRED"},
        {'name': "title", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "original_title", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "overview", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "original_lang", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "poster_img_path", 'type': "STRING", 'mode': "NULLABLE"},
        {'name': "genres", 'type': "STRING", 'mode': "REPEATED"},
        {'name': "casting", 'type': "RECORD", 'mode': "REPEATED", "fields": [
            {'name': "name", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "original_name", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "character", 'type': "STRING", 'mode': "NULLABLE"},
        ]},
        {'name': "seasons", 'type': "RECORD", 'mode': "REPEATED", "fields": [
            {'name': "number", 'type': "INT64", 'mode': "NULLABLE"},
            {'name': "name", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "number_episodes", 'type': "INT64", 'mode': "NULLABLE"},
            {'name': "air_date", 'type': "STRING", 'mode': "NULLABLE"},
        ]},
        {'name': "external_ids", 'type': "RECORD", 'mode': "NULLABLE", "fields": [
            {'name': "imdb_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "tvdb_id", 'type': "INT64", 'mode': "NULLABLE"},
            {'name': "facebook_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "instagram_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "twitter_id", 'type': "STRING", 'mode': "NULLABLE"},
        ]},
        {'name': "created_at", 'type': "DATETIME", 'mode': "REQUIRED"},
    ]}


def fetch_movies_schema() -> Dict:
    return {'fields': [
        {'name': "id", 'type': "INT64", 'mode': "REQUIRED"},
        {'name': "title", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "original_title", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "overview", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "original_lang", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "poster_img_path", 'type': "STRING", 'mode': "NULLABLE"},
        {'name': "release_date", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "genres", 'type': "STRING", 'mode': "REPEATED"},
        {'name': "casting", 'type': "RECORD", 'mode': "REPEATED", "fields": [
            {'name': "name", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "original_name", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "character", 'type': "STRING", 'mode': "NULLABLE"},
        ]},
        {'name': "external_ids", 'type': "RECORD", 'mode': "NULLABLE", "fields": [
            {'name': "imdb_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "facebook_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "instagram_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "twitter_id", 'type': "STRING", 'mode': "NULLABLE"},
        ]},
        {'name': "is_adult", 'type': "BOOL", 'mode': "REQUIRED"},
        {'name': "created_at", 'type': "DATETIME", 'mode': "REQUIRED"},
    ]}


def run():
    app()


if __name__ == "__main__":
    run()
