from typing import NamedTuple

from src.api_handler import sp
from src import db

from src import api_handler as api
from src.api_handler.playlists import Playlist
from src.controller.update_db import update_all_playlist_tracks_in_db
from src.controller import playlist_change_detection as pcd
from src.helpers.myers import Myers
from src.settings.user_data import get_playlist_user_data
from src.types.playlists import AllPlaylists

# TODO move this to settings.json or .env
SNIPPET_SIZE = 50


def sync_playlist_pair(main: AllPlaylists, snippet: AllPlaylists):
	#################### this function needs to know about the changes
	# that happened in the playlists. This means update_playlist_tracks_in_db
	# cannot finish running before this function started
	"""
	compare main and snippet playlists and see what has changed and
	update both playlists approriately
	"""
	# prerequisite: know which playlists have changed
	# if only main or snippet changed:
	# 	add changes to other playlist
	# if both playlists changed:
	# 	get difference between both and update playlists
	# update database

	snippet_changed = pcd.has_playlist_changed(snippet)
	main_changed = pcd.has_playlist_changed(main)
	if not main_changed and snippet_changed:
		return

	snippet_playlist = api.playlists.Playlist(snippet)
	main_playlist = api.playlists.Playlist(main)

	if snippet_changed:
		snippet_diff = pcd.get_track_diff(snippet)
		main_playlist.add_tracks_at_end(snippet_diff.inserts)
		main_playlist.remove_tracks(snippet_diff.removals)

		# TEST: wait? In case it needs some time to propagate

	copy_tracks_to_snippet(main_playlist, snippet_playlist)

def copy_tracks_to_snippet(main: api.playlists.Playlist, snippet: api.playlists.Playlist):
	main_latest_tracks = main.get_latest_tracks(SNIPPET_SIZE)
	snippet.replace_tracks(main_latest_tracks)

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
	algorithm can be seen in test_myers.test_diffing_changes_before()
	basically: get changes in a_lines and b_lines and do all changes
	on other playlist respectively
	"""
	# get changes in snippet playlist
	# apply changes to main playlist
	# copy latest tracks from main to snippet
	