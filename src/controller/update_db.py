from src import db
from src import api
from src.api.playlists import PlaylistHandler, PlaylistsHandler
from src.controller import playlist_change_detection as pcd



def update_db_liked_tracks():
	""" careful! This iterates though all liked tracks
			and is therefore very expensive rate limiting wise """
	# TODO: finish
	liked_db_tracks = db.tracks.get_liked_tracks()
	gen = api.get_liked_tracks_generator()
	# for batch in gen:
	# 	tracks = batch.tracks
		
	# 	db.tracks.add_tracks(tracks, liked=True)


def update_playlist_tracks_in_db(playlist: PlaylistHandler, diff: pcd.Diff | None=None):
	""" playlist should be very up to date """
	# TEST: check if this function works for an empty playlist that has just been added

	if not pcd.has_playlist_changed(playlist.data):
		return

	db.playlists.update_playlists([playlist.data])

	if diff is None:
		diff = pcd.get_playlist_diff(playlist)
	db.playlists.remove_tracks_from_playlist(playlist.id, diff.removals)
	db.playlists.add_tracks_to_playlist(playlist.id, diff.inserts)
	return diff

	
def update_all_playlist_tracks_in_db():
	playlists = PlaylistsHandler()
	# changed = pcd.get_changed_playlists(playlists)
	for playlist in playlists.playlists:
		update_playlist_tracks_in_db(playlist)