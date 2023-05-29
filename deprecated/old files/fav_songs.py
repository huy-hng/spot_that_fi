import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import helpers
import settings # pylint: disable=unused-import
from logger import log
# pylint: disable=logging-fstring-interpolation


redirect_uri = 'http://localhost:8080/'
scope = 'user-top-read playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
																								client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
																								redirect_uri=redirect_uri, scope=scope))


short_term_uri = 'spotify:playlist:712DuDhRyAN5W7eONBwByP'
medium_term_uri = 'spotify:playlist:4xQrCR2AqL7I8nVL6McUJP'
long_term_uri = 'spotify:playlist:0qELV6Dtv3X0j6qMusYsDT'

get_track_ids = lambda tracks: [track['id'] for track in tracks]

def main():
	limit = 50
	short_tracks = sp.current_user_top_tracks(limit=limit, time_range='short_term')['items']
	medium_tracks = sp.current_user_top_tracks(limit=limit, time_range='medium_term')['items']
	long_tracks = sp.current_user_top_tracks(limit=limit, time_range='long_term')['items']

	sp.playlist_replace_items(short_term_uri, get_track_ids(short_tracks))
	sp.playlist_replace_items(medium_term_uri, get_track_ids(medium_tracks))
	sp.playlist_replace_items(long_term_uri, get_track_ids(long_tracks))

main()