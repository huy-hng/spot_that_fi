import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# pylint: disable=unused-import
# pylint: disable=logging-fstring-interpolation
import helpers
import settings 
from logger import log



redirect_uri = 'http://localhost:8080/'
scope = 'playlist-modify-private playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
																								client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
																								redirect_uri=redirect_uri, scope=scope))

all_playlists = sp.current_user_playlists()

if __name__ == '__main__':
	from create_small_playlists import check_for_changes, PlaylistType

	log.info('')
	check_for_changes(PlaylistType.ALL)
	# check_for_changes(PlaylistType.SNIPPET)
 