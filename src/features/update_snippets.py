from src.controller.update_functions import update_db_all_playlists
from src.db.playlists import get_track_ids


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
	update_db_all_playlists()

	# get all main and snippet uris

	uris = []
	for uri in uris:
		tracks = get_track_ids(uri)


def sync_snippet_playlists():
	# get changed playlists
	# for changed in changed_playlists
	# replace snippet playlists tracks with x amount of tracks from main playlist
	# update db playlists accordingly
	...


def 