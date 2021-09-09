import os
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
load_dotenv()

from helpers import get_track_names

# from logger import log
# pylint: disable=logging-fstring-interpolation



# redirect_uri = 'http://localhost:8080/'
redirect_uri = 'http://localhost/'
# scope = 'playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative'
scope = 'playlist-modify-private playlist-read-private playlist-modify-public'
# scope = 'playlist-modify-private playlist-read-private'
sp = spotipy.Spotify(
	auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
														client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
														redirect_uri=redirect_uri, scope=scope))

all_playlists = sp.current_user_playlists() # TODO: incase I have more playlists than the
# limit allows, create a function to fetch all playlists
with open('./data/playlists.json', 'w') as f:
	f.write(json.dumps(all_playlists))


if __name__ == '__main__':
	with open('./data/playlists.json') as f:
		all_playlists = json.loads(f.read())

	from playlist_handler import Playlists

	playlists = Playlists(all_playlists).playlists

	calm = playlists['Calm All']
	tracks = calm.get_latest_tracks(30)
	tracks = get_track_names(tracks)

	print(tracks)
 