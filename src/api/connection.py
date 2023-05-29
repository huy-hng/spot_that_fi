import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
load_dotenv()

redirect_uri = 'http://localhost:8080/'
scope = ''
scope += 'playlist-read-private '
scope += 'playlist-modify-private '
scope += 'playlist-modify-public '
scope += 'playlist-read-collaborative'

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
		client_id=os.getenv('SPOTIPY_CLIENT_ID'),
		client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
		redirect_uri=redirect_uri, scope=scope))
