from dataclasses import dataclass


@dataclass
class SearchResult:
    id: str
    media_type: str
    title: str
    original_title: str
    overview: str
    original_lang: str
    release_date: str
    is_adult: bool

    def __init__(self, **kwargs):
        """
        - media_type is either 'movie' or 'tv'
        - title/original_title apply only for movies
        - name/original_name apply only for tv_shows
        """

        self.id = kwargs.get('id')
        self.media_type = kwargs.get('media_type')
        self.title = kwargs.get('title') or kwargs.get('name')
        self.original_title = kwargs.get('original_title') or kwargs.get('original_name')
        self.overview = kwargs.get('overview')
        self.original_lang = kwargs.get('original_language')
        self.release_date = kwargs.get('release_date')
        self.is_adult = kwargs.get('adult') or False
