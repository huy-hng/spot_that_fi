import json

from src.helpers.helpers import read_data, write_data
from src import api
from src.helpers.logger import log

def write_liked_tracks():
	gen = api.get_liked_tracks_generator()
	tracks = []
	for i, batch in enumerate(gen):
		log.info(f'Batch {i} for adding liked tracks')

		tracks += batch

	write_data('liked_tracks', tracks)


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