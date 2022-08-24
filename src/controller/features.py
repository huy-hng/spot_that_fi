from src import db
from src.api_handler import sp
from src.helpers.logger import log
from src.controller import update_functions

""" 

before each function, update_db_playlists should be called
so that all operations are up to date with spotify

"""


def update_liked_tracks_not_in_playlists_playlist():
	""" this function updates the playlist that containes songs
			that are liked, but not in any other playlists
			(except for this one)\n
			tracks is a list with track ids """

	playlist_id = None # TODO
	# TODO: uncomment lines below
	# update_functions.update_db_liked_tracks()
	track_ids = db.tracks.get_liked_tracks_not_in_playlists()
	log.debug(track_ids)
	# sp.replace_playlist_tracks(playlist_id, track_ids)
	

def like_tracks_in_playlists():
	# TODO: uncomment lines below
	# update_functions.update_db_liked_tracks()
	# update_functions.update_db_playlists()
	track_ids = db.tracks.get_not_liked_tracks_in_playlists()
	log.debug(track_ids)
	# sp.like_tracks(track_ids)


def update_snippet_and_archive():
	pass
	