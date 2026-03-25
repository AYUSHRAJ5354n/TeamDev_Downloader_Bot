from .YouTube   import fetch_youtube,  is_valid_youtube_url
from .multi_down import fetch_multi
from .Terabox   import fetch_terabox,  is_valid_terabox_url
from .Vimeo     import fetch_vimeo,    is_valid_vimeo_url
from .Spotify   import fetch_spotify,  is_valid_spotify_url

__all__ = [
    "fetch_youtube",  "is_valid_youtube_url",
    "fetch_multi",
    "fetch_terabox",  "is_valid_terabox_url",
    "fetch_vimeo",    "is_valid_vimeo_url",
    "fetch_spotify",  "is_valid_spotify_url",
]
