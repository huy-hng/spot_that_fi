import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import settings # pylint: disable=unused-import
from logger import log
# pylint: disable=logging-fstring-interpolation



# redirect_uri = 'http://localhost:8080/'
redirect_uri = 'http://localhost/'
# scope = 'playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative'
scope = 'playlist-modify-private playlist-read-private playlist-modify-public'
# scope = 'playlist-modify-private playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
																								client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
																								redirect_uri=redirect_uri, scope=scope))

all_playlists = sp.current_user_playlists()

if __name__ == '__main__':
	from create_small_playlists import check_for_changes, PlaylistType

	log.info('')
	check_for_changes(PlaylistType.ALL)
	# check_for_changes(PlaylistType.SNIPPET)
 