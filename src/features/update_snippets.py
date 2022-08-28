from src.api_handler import sp
from src import api_handler as api
from src.controller.update_functions import update_all_playlist_tracks_in_db
from src.db.playlists import get_track_ids
from src.controller import playlist_change_detection as pcd
from types.playlists import AllPlaylists

# TODO move this to settings.json or .env
SNIPPET_SIZE = 50

def update_sp_snippet_playlists():
	""" 
	update all db playlists
	get tracks from appropriate playlist in db
	replace all tracks in playlist on spotify

	alternate solution:
	get x latest tracks directly from spotify
	replace all tracks in playlist in spotify

	this solution might be more friendly for rate limiting since
	one doesnt need to update all playlists just to get
	the snippet playlists
	"""
	update_all_playlist_tracks_in_db()

	# get all main and snippet uris

	uris = []
	for uri in uris:
		tracks = get_track_ids(uri)


def sync_playlist_pair(main: AllPlaylists, snippet: AllPlaylists):
	# prerequisite: know which playlists have changed
	# if only main or snippet changed:
	# 	add changes to other playlist
	# if both playlists changed:
	# 	get difference between both and update playlists
	# update database
	...

	main_changed = pcd.has_playlist_changed(main)
	snippet_changed = pcd.has_playlist_changed(snippet)

	if main_changed and snippet_changed:
		... # TODO
	elif main_changed:
		... # copy last x tracks from main to snippet
		gen = sp.get_playlist_tracks_generator(main.id)
	elif snippet_changed:
		... # get diff between snippet and main
	else:
		... # nothing changed and can be skipped


def sync_all_playlists():
	""" bulk logic is in sync_playlists """
	all_sp_playlists = sp.get_all_playlists()
	playlists = api.Playlists(all_sp_playlists)

	for pair in playlists.get_sync_pairs():
		sync_playlist_pair(pair.main, pair.snippet)

