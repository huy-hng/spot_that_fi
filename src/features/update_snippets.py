from typing import NamedTuple

from src.api_handler import sp
from src import db

from src import api_handler as api
from src.controller.update_db import update_all_playlist_tracks_in_db
from src.controller import playlist_change_detection as pcd
from src.helpers.myers import Myers
from src.settings.user_data import get_playlist_user_data
from src.types.playlists import AllPlaylists

# TODO move this to settings.json or .env
SNIPPET_SIZE = 50


def sync_playlist_pair(main: AllPlaylists, snippet: AllPlaylists):
	"""
	TODO: sync playlists without knowing wether they have changed or not.
	compare main and snippet playlists and see what has changed and
	update both playlists approriately
	"""
	# prerequisite: know which playlists have changed
	# if only main or snippet changed:
	# 	add changes to other playlist
	# if both playlists changed:
	# 	get difference between both and update playlists
	# update database

	main_changed = pcd.has_playlist_changed(main)
	snippet_changed = pcd.has_playlist_changed(snippet)

	if main_changed and snippet_changed:
		... # TODO
	elif main_changed:
		# copy last x tracks from main to snippet
		main_playlist = api.playlists.Playlist(main)
		tracks = main_playlist.get_latest_tracks(SNIPPET_SIZE)

		snippet_playlist = api.playlists.Playlist(snippet)
		snippet_playlist.replace_tracks(tracks)
			
	elif snippet_changed:
		... # get diff between snippet and main
		pcd.get_track_diff()
	else:
		... # nothing changed and can be skipped


class SyncPairs(NamedTuple):
	main: db.tables.Playlist
	snippet: db.tables.Playlist

def sync_all_playlists():
	"""
	update all db playlists
	get tracks from appropriate playlist in db
	replace all tracks in playlist on spotify

	bulk logic is in sync_playlists
	"""

	update_all_playlist_tracks_in_db()

	pairs: list[SyncPairs] = []
	playlist_data = get_playlist_user_data()
	snippet_data = playlist_data['snippet_playlist']
	for data in snippet_data:
		main_track_ids = db.playlists.get_track_ids(data['main_uri'])
		snippet_track_ids = db.playlists.get_track_ids(data['snippet_uri'])

		myers = Myers(snippet_track_ids, main_track_ids)
		myers.index_of_first_keep

	# all_sp_playlists = sp.get_all_playlists()
	# playlists = api.Playlists(all_sp_playlists)
	for pair in playlists.get_sync_pairs():
		sync_playlist_pair(pair.main, pair.snippet)

def sync_algorithm():
	""" 

	
	"""
	...