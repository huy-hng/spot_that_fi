from src import db
from src.api_handler import sp
from src.helpers.logger import log
from src.controller import playlist_change_detection
from src.types.playlists import SpotifyPlaylistType



def update_db_liked_tracks():
	""" careful! This iterates though all liked tracks
			and is therefore very expensive rate limiting wise """
	gen = sp.get_liked_tracks_generator()
	for batch in gen:
		db.tracks.add_tracks(batch, liked=True)


def update_playlist_tracks_in_db(playlist: SpotifyPlaylistType):
	""" playlist should be very up to date """
	# TODO: check if this function works for an empty playlist that has just been added

	# TODO: might be redundant if db.playlists.add_playlists also updates the playlist
	# if it exists
	db.playlists.update_playlist(playlist) 

	removals, inserts = playlist_change_detection.get_track_diff(
												playlist.id, playlist.tracks.total)
	db.playlists.remove_tracks_from_playlist(playlist.id, removals)
	db.playlists.add_tracks_to_playlist(playlist.id, inserts)

	
def update_all_playlist_tracks_in_db():
	playlists = sp.get_all_playlists()
	db.playlists.add_playlists(playlists)
	changed = playlist_change_detection.get_changed_playlists()
	for playlist in changed:
		update_playlist_tracks_in_db(playlist)