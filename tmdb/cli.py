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
        tbl_spec = "cast_movies"
        movies = (pipeline
                  | beam.Create(movies)
                  | beam.Map(lambda movie: movie_api.get_details(movie.id).to_dict())
                  | beam.io.WriteToBigQuery(tbl_spec,
                                            schema=fetch_movies_schema(),
                                            write_disposition=BQDisposition.WRITE_APPEND,
                                            create_disposition=BQDisposition.CREATE_IF_NEEDED,
                                            custom_gcs_temp_location="gs://temp-bucket/")
                  )


def fetch_movies_schema() -> Dict:
    return {'fields': [
        {'name': "id", 'type': "INT64", 'mode': "REQUIRED"},
        {'name': "title", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "original_title", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "overview", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "original_lang", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "poster_img_path", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "release_date", 'type': "STRING", 'mode': "REQUIRED"},
        {'name': "genres", 'type': "STRING", 'mode': "REPEATED"},
        {'name': "external_ids", 'type': "RECORD", 'mode': "REPEATED", "fields": [
            {'name': "imdb_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "facebook_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "instagram_id", 'type': "STRING", 'mode': "NULLABLE"},
            {'name': "twitter_id", 'type': "STRING", 'mode': "NULLABLE"},
        ]},
        {'name': "is_adult", 'type': "BOOL", 'mode': "REQUIRED"},
    ]}


def run():
    app()


if __name__ == "__main__":
    run()
