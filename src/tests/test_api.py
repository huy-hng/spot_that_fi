import pytest

from src.api_handler import sp
from src.api_handler.playlists import PlaylistsHandler, PlaylistHandler
from src.helpers.helpers import print_dict
from src.tests import PlaylistIDs

def test_get_liked_tracks():
	for items in sp.get_liked_tracks_generator():
		# print(items)
		break

def test_get_one_playlist():
	playlist = sp.get_one_playlist(PlaylistIDs.unchanged)
	# playlist.

def test_add_tracks_to_playlist():
	playlists = sp.get_all_playlists()
	playlists_handler = PlaylistsHandler(playlists)
	# for items in sp.get_playlist_tracks_generator('6BDxVpN7v1HFSRGgt8LYC8'):
	# 	print(items)
	# 	break
	unchanged = playlists_handler.get_by_id(PlaylistIDs.unchanged)


@pytest.mark.parametrize(
	'total,limit,expected', [
		(100, 100, (100,)),
		(100, 34, (34,34,32)),
		(80, 34, (34,34,32)),
		(999, 34, (34,34,32)),
		(0, 34, (34,34,32)),

		(100, 0, [1 for _ in range(100)]), # special case
		(100, 2, [2 for _ in range(100)]), # special case
		(100, 200, (100,)),
	]
)
def test_get_playlist_tracks_generator(
	playlists_handler: PlaylistsHandler, total: int, limit: int, expected: tuple[int]):

	unchanged = playlists_handler.get_by_id(PlaylistIDs.unchanged)
	gen = sp.get_playlist_tracks_generator(unchanged.id, total,limit=limit)
	for i, items in enumerate(gen):
		assert len(items.items_) == expected[i]
		if i == 3:
			break