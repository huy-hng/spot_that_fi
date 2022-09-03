from src.api_handler import sp
from src.tests import PlaylistIDs


def test_get_liked_tracks():
	for items in sp.get_liked_tracks_generator():
		print(items)
		break

def test_get_one_playlist():
	playlist = sp.get_one_playlist(PlaylistIDs.unchanged)
	# playlist.
