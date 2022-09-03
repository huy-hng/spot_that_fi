
from src.api_handler import sp
from src import db

from src import api_handler as api
from src.controller.update_db import update_all_playlist_tracks_in_db
from src.controller import playlist_change_detection as pcd
from src.helpers.myers import Myers
from src.settings.user_data import get_playlist_user_data
from src.types.playlists import AllPlaylists, SinglePlaylist

# TODO move this to settings.json or .env
SNIPPET_SIZE = 50


# TODO: possibility to put in playlist_id instead of instace of a playlist class
def sync_playlist_pair(
	main: AllPlaylists | SinglePlaylist,
	snippet: AllPlaylists | SinglePlaylist,
	*, snippet_size=SNIPPET_SIZE):
	"""
	compare main and snippet playlists and see what has changed and
	update both playlists approriately
	"""
	#################### this function needs to know about the changes
	# that happened in the playlists. This means update_playlist_tracks_in_db
	# cannot finish running before this function started

	snippet_changed = pcd.has_playlist_changed(snippet)
	main_changed = pcd.has_playlist_changed(main)
	if not main_changed and snippet_changed:
		return

	snippet_playlist = api.playlists.Playlist(snippet)
	main_playlist = api.playlists.Playlist(main)

	if snippet_changed:
		snippet_diff = pcd.get_playlist_diff(snippet)
		main_playlist.add_tracks_at_end(snippet_diff.inserts)
		sp.remove_tracks(main_playlist.id, snippet_diff.removals)

		# TEST: wait? In case it needs some time to propagate

	main_latest_tracks = main_playlist.get_latest_tracks(snippet_size)
	snippet_playlist.replace_tracks(main_latest_tracks)

	# TODO think about where to add database update


def sync_all_playlists():
	"""
	update all db playlists
	get tracks from appropriate playlist in db
	replace all tracks in playlist on spotify

	bulk logic is in sync_playlists
	"""

	all_sp_playlists = sp.get_all_playlists()
	playlists = api.Playlists(all_sp_playlists)

	for pair in playlists.get_sync_pairs():
		sync_playlist_pair(pair.main, pair.snippet)
