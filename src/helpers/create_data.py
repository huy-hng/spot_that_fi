import json

from src.helpers.helpers import read_dict_from_file, write_dict_to_file
from src.api import sp
from src.helpers.logger import log

def write_liked_tracks():
	gen = sp.get_liked_tracks_generator()
	tracks = []
	for i, batch in enumerate(gen):
		log.info(f'Batch {i} for adding liked tracks')

		tracks += batch

	write_dict_to_file('liked_tracks', tracks)


def write_tracks_in_playlists():
	...
	# with open('./data/playlists.json') as f:
	# 	playlists = json.loads(f.read())

	# for j, playlist in enumerate(playlists):
	# 	playlist_id = playlist['id']

	# 	gen = sp.get_playlist_tracks_generator(playlist_id)
	# 	tracks = []
	# 	for i, batch in enumerate(gen):
	# 		log.info(f'Batch {i} for playlist {playlist["name"]}')
	# 		tracks += batch
	# 		# break

	# 	write_dict_to_file(f'playlists/{playlist_id}', tracks)
