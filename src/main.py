import os
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
load_dotenv()

# from logger import log
# pylint: disable=logging-fstring-interpolation



# redirect_uri = 'http://localhost:8080/'
redirect_uri = 'http://localhost/'
scope = 'playlist-modify-private playlist-read-private'
sp = spotipy.Spotify(
	auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
														client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
														redirect_uri=redirect_uri, scope=scope))

# all_playlists = sp.current_user_playlists()


if __name__ == '__main__':
	with open('./data/playlists.json') as f:
		all_playlists = json.loads(f.read())


	tracks = sp.playlist_items('spotify:playlist:2OBconDUKoGs6BoDTVMVvk',
										fields='items',
										limit=100,
										offset=40
										)['items']


	print(tracks)
	# from playlist_handler import Playlists
	# playlists = Playlists(all_playlists).playlists

	# calm = playlists['Calm']
	# calm.get_tracks(114)

# 	from create_small_playlists import check_for_changes, PlaylistType

# 	log.info('')
# 	check_for_changes(PlaylistType.ALL)
	# check_for_changes(PlaylistType.SNIPPET)
 