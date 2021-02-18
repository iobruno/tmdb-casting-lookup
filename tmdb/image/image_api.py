import os
import requests as r
from typing import Dict

from tmdb.movies.movie import MovieDetails


class ImageApi:

    def __init__(self, bearer_token: str = os.environ['TMDB_API_KEY']):
        self.bearer_token = bearer_token
        self.image_endpoint = "https://www.themoviedb.org/t/p/"

    def get_picture(self, image_id: str, size: str):
        image = r.get(f"{self.image_endpoint}/{size}/{image_id}",
                      headers={"Authorization": f"Bearer {self.bearer_token}"})

    def get_profile_picture(self, image_id: str, profile_img_size: str = "w185"):
        """
        :param image_id: TMDB image id
        :param profile_img_size: Width or Height of the image requested
                                 Available profile_img_size options:
                                 ['w45', 'w185', 'h632', 'original']
        """
        return self.get_picture(image_id, profile_img_size)

    def get_poster_picture(self, image_id: str, poster_img_size: str = "w780"):
        """
        :param image_id: TMDB image id
        :param poster_img_size: Width or Height of the image requested
                                Available poster_img_size options:
                                'w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original'
        """
        return self.get_picture(image_id, poster_img_size)
