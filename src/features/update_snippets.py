from src.api_handler import sp
from src.controller.update_functions import update_all_playlist_tracks_in_db
from src.db.playlists import get_track_ids
from src import db
from src.controller import playlist_change_detection
from src import playlists

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


def sync_snippet_playlists():
	# get playlists to snippet
	# get changed playlists
	# for changed in changed_playlists
	# replace snippet playlists tracks with x amount of tracks from main playlist
	# update db playlists accordingly
	snippet_playlists = playlists.tracked
	changed_playlists = playlist_change_detection.get_changed_playlists()
	for changed in changed_playlists:

		pass

def sync_playlists(main_id: str, snippet_id: str):

	