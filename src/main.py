import os
import json

from helpers import get_track_names
from backup import backup_all_playlists

# from logger import log
# pylint: disable=logging-fstring-interpolation

if __name__ == '__main__':
	with open('./data/playlists.json') as f:
		all_playlists = json.loads(f.read())

	from playlist_handler import Playlists


	playlists = Playlists()
	# backup_all_playlists(playlists)

	# print(f'api calls: {sp.api_calls}')
 