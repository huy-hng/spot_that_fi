from .api_handler import Spotipy

sp = Spotipy()

from api.tracks import Tracks
from api.playlists import PlaylistHandler, PlaylistsHandler