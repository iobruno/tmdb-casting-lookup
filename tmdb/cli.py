from pathlib import Path
from typing import Dict

import apache_beam as beam
import typer
from apache_beam.io import BigQueryDisposition
from PIL import UnidentifiedImageError

from tmdb.image.gcs_api import GCSApi
from tmdb.image.image_api import ImageApi
from tmdb.movies.movie_api import MovieApi, MovieDetails
from tmdb.search.search_api import SearchApi
from tmdb.tv.tv_show_api import TvShowApi
from tmdb.utils.config import Configuration
from tmdb.utils.logger import get_logger

app = typer.Typer()
logger = get_logger("CLI App")

logger.info("Loading configuration file")
config_file = Path(__file__).parent.parent.joinpath("application.yml")
cfg = Configuration.load_config(config_file, profile="prod")


@app.command("discover")
def discover_and_fetch():
    NotImplemented("Discover is not yet implemented")


def fetch_and_upload_images(p: MovieDetails):
    """Production may refer to either a Movie or TVShow"""
    image_api = ImageApi()
    gcs = GCSApi()

    for cast in p.casting:
        try:
            logger.info(f"Fetching profile picture for {cast.name}...")
            pic = image_api.get_profile_picture(cast.pfp)

            blob_name = f"movies/{p.id}/casting/{cast.name}.jpg"
            cast.profile_img_path = gcs.image_upload(pic, blob_name)
            logger.info(f"Image successfully Uploaded to {cast.profile_img_path}")
        except UnidentifiedImageError:
            logger.warn("Could not find an image for id: {name} (character). Skipping..."
                        .format(name=cast.name, character=cast.character))

    logger.info(f"Fetching poster picture for '{p.title}'...")
    pic = image_api.get_poster_picture(p.poster_img_path)
    blob_name = f"movies/{p.id}/poster/{p.original_title}.jpg"

    p.poster_img_path = gcs.image_upload(pic, blob_name)
    logger.info(f"Image successfully Uploaded to {p.poster_img_path}")

    return p


@app.command("search")
def search_and_fetch(query: str = typer.Option(..., "-q", "--query",
                                               help="Query movies, tv shows by name")):
    logger.info(f"Querying DB for Movies and TV Show with '{query}'")
    search_results = SearchApi().query(query_string=query)
    movies_results = search_results.get('movie', [])
    tv_shows_results = search_results.get('tv', [])

    movie_api, tv_api = MovieApi(), TvShowApi()

    with beam.Pipeline() as pipeline:
        movies = (pipeline
                  | beam.Create(movies_results)
                  | beam.Map(lambda movie_result: movie_api.get_details(movie_result.id))
                  | beam.Map(fetch_and_upload_images)
                  | beam.Map(lambda movie: movie.to_bq())
                  )

        movies | beam.io.WriteToBigQuery(cfg.gcloud.casting_movies_table,
                                         schema=fetch_movies_schema(),
                                         write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
                                         create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
                                         custom_gcs_temp_location=cfg.gcloud.gcs_to_bq_temp)


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
            {'name': "profile_img_path", 'type': "STRING", 'mode': "NULLABLE"},
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
