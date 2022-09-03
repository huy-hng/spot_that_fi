from src.api_handler import sp
from src.api_handler.playlists import PlaylistsHandler
from src.tests import PlaylistIDs


def test_get_liked_tracks():
	for items in sp.get_liked_tracks_generator():
		print(items)
		break

def test_get_one_playlist():
	playlist = sp.get_one_playlist(PlaylistIDs.unchanged)
	# playlist.

def test_add_tracks_to_playlist():
	playlists = sp.get_all_playlists()
	playlists_handler = PlaylistsHandler(playlists)
	
	
	