import json
from src.helpers.helpers import read_dict_from_file, write_dict_to_file


from src.helpers.logger import log
from src.db.features import get_latest_tracks_added_to_playlists
from src.api_handler.api_handler import Spotipy

from src.tests import test_database, test_diff

with open('./data/playlists.json') as f:
	playlists = json.loads(f.read())

sp = Spotipy()

def add_playlists():
	db.add_playlists(playlists)

def add_tracks_to_playlist():

	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'

	generator = sp.get_playlist_tracks_generator(playlist_id)
	for i, batch in enumerate(generator):
		log.info(f'Batch {i} for adding playlist tracks')
		db.add_tracks_to_playlist(playlist_id, batch)
		if i == 2:
			break


def add_liked_tracks():
	gen = sp.get_liked_tracks_generator()
	for i, batch in enumerate(gen):
		log.info(f'Batch {i} for adding liked tracks')
		db.add_tracks(batch, liked=True)
		if i == 10:
			break


def write_liked_tracks():
	gen = sp.get_liked_tracks_generator()
	tracks = []
	for i, batch in enumerate(gen):
		log.info(f'Batch {i} for adding liked tracks')

		tracks += batch

	write_dict_to_file('liked_tracks', tracks)

def write_tracks_in_playlists():
	with open('./data/playlists.json') as f:
		playlists = json.loads(f.read())

	for j, playlist in enumerate(playlists):
		playlist_id = playlist['id']

		gen = sp.get_playlist_tracks_generator(playlist_id)
		tracks = []
		for i, batch in enumerate(gen):
			log.info(f'Batch {i} for playlist {playlist["name"]}')
			tracks += batch
			# break

		write_dict_to_file(f'playlists/{playlist_id}', tracks)


if __name__ == '__main__':
	# add_liked_tracks()
	# add_tracks_to_playlist()
	# tracks = db.get_not_liked_tracks()
	# for track in tracks:
	# 	print(track)
	# write_liked_tracks()
	# write_tracks_in_playlists()

	# test_database.add_tracks_to_all_playlists()
	# test_database.add_liked_tracks()
	# test_database.liked_tracks_not_in_playlists()
	# test_database.get_playlist_tracks('Tech House')

	# tech_house = '0oWDXsY9BhT9NKimKwNY9d'
	test_diff.diff()
