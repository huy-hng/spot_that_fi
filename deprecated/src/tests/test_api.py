import time
import pytest
import dataclasses

from src import api
from src.api.playlists import PlaylistsHandler, get_ids
from src.tests import PlaylistIDs
from src.helpers.helpers import write_data


def get_liked_tracks():
	responses = []
	for items in api.get_liked_tracks_generator():
		d = dataclasses.asdict(items)
		responses.append(d)
		time.sleep(0.1)
		break

	# write_dict_to_file('asdict_liked_track_list', responses)


def test_get_one_playlist():
	playlist = api.get_playlist(PlaylistIDs.unchanged)
	# playlist.


@pytest.mark.parametrize(
	'group_size', [
		0, 1, 3, 5, 10
	]
)
def test_add_tracks_to_playlist(playlists_handler: PlaylistsHandler, group_size: int):
	unchanged = playlists_handler.get_by_id(PlaylistIDs.unchanged)
	main = playlists_handler.get_by_id(PlaylistIDs.main)

	main.replace_tracks([])

	num = 5

	tracks_to_add = unchanged.get_latest_tracks(num)
	main.add_tracks_at_end(tracks_to_add, group_size)

	expected = get_ids(tracks_to_add)
	result = get_ids(main.get_latest_tracks(num))
	assert result == expected


@pytest.mark.parametrize(
	'total,limit,expected', [
		(100, 100, (100,)),
		(100, 34, (34, 34, 32)),
		(80, 34, (34, 34, 32)),
		(999, 34, (34, 34, 32)),
		(0, 34, (34, 34, 32)),

		(100, 0, [1 for _ in range(100)]),  # special case
		(100, 2, [2 for _ in range(100)]),  # special case
		(100, 200, (100,)),
	]
)
def test_get_playlist_tracks_generator(
	playlists_handler: PlaylistsHandler, total: int, limit: int, expected: tuple[int]):

	unchanged = playlists_handler.get_by_id(PlaylistIDs.unchanged)
	unchanged.total_tracks = total
	gen = unchanged.get_track_generator(limit=limit)
	for i, items in enumerate(gen):
		assert len(items) == expected[i]
		if i == 3:
			break