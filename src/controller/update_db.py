from src import db
from src.api_handler import sp
from src.helpers.logger import log
from src.controller import playlist_change_detection as pcd
from src.types.playlists import AllPlaylists, SinglePlaylist, AbstractPlaylistType



def update_db_liked_tracks():
	""" careful! This iterates though all liked tracks
			and is therefore very expensive rate limiting wise """
	gen = sp.get_liked_tracks_generator()
	for batch in gen:
		tracks = batch.tracks
		
		db.tracks.add_tracks(tracks, liked=True)


def update_playlist_tracks_in_db(playlist: AllPlaylists):
	""" playlist should be very up to date """
	# TEST: check if this function works for an empty playlist that has just been added

	if not pcd.has_playlist_changed(playlist):
		return

	db.playlists.update_playlists([playlist])

	removals, inserts = pcd.get_track_diff(playlist)
	db.playlists.remove_tracks_from_playlist(playlist.id, removals)
	db.playlists.add_tracks_to_playlist(playlist.id, inserts)

	
def update_all_playlist_tracks_in_db():
	playlists = sp.get_all_playlists()
	# changed = pcd.get_changed_playlists(playlists)
	for playlist in playlists:
		update_playlist_tracks_in_db(playlist)