from src.api_handler import sp


def test_get_liked_tracks():
	for items in sp.get_liked_tracks_generator():
		print(items)
		break