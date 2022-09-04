from src import api
from src.controller import playlist_change_detection as pcd
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

	snippet_playlist = api.PlaylistHandler(snippet)
	main_playlist = api.PlaylistHandler(main)

	if snippet_changed:
		snippet_diff = pcd.get_playlist_diff(snippet_playlist)
		main_playlist.add_tracks_at_end(snippet_diff.inserts)
		main_playlist.remove_tracks(snippet_diff.removals)

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

	playlists = api.PlaylistsHandler()

	for pair in playlists.get_sync_pairs():
		sync_playlist_pair(pair.main, pair.snippet)
