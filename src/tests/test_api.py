import pytest

from src import api
from src.api import PlaylistsHandler, PlaylistHandler
from src.helpers.helpers import print_dict
from src.tests import PlaylistIDs

def test_get_liked_tracks():
	for items in api.get_liked_tracks_generator():
		# print(items)
		break

def test_get_one_playlist():
	playlist = api.get_one_playlist(PlaylistIDs.unchanged)
	# playlist.

def test_add_tracks_to_playlist(playlists_handler: PlaylistsHandler):
	unchanged = playlists_handler.get_by_id(PlaylistIDs.unchanged)
	main = playlists_handler.get_by_id(PlaylistIDs.main)

	main.replace_tracks([])

	num = 10

	tracks_to_add = unchanged.get_latest_tracks(num)
	main.add_tracks_at_end(tracks_to_add, 2)

	expected = PlaylistHandler.get_ids(tracks_to_add)
	result = PlaylistHandler.get_ids(main.get_latest_tracks(num))
	assert result == expected


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
	gen = api.get_playlist_tracks_generator(unchanged.id, total,limit=limit)
	for i, items in enumerate(gen):
		assert len(items.items_) == expected[i]
		if i == 3:
			break