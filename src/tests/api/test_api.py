import time
import pytest
import dataclasses

from src import api
from src import log
from src.tests import PlaylistIDs
from src.utils import write_data


def get_liked_tracks():
	responses = []
	for items in api.get_liked_tracks_generator():
		d = dataclasses.asdict(items)
		responses.append(d)
		time.sleep(0.1)
		break

	# write_data('asdict_liked_track_list', responses)


def test_get_playlist():
	playlist = api.get_playlist(PlaylistIDs.unchanged)
	log.info(playlist)
	
@pytest.mark.parametrize(
	'group_size', [
		0, 1, 3, 5, 10
	]
)
def test_add_tracks_to_playlist(playlists_manager: api.PlaylistsManager, group_size: int):
	unchanged = playlists_manager.get_by_id(PlaylistIDs.unchanged)
	main = playlists_manager.get_by_id(PlaylistIDs.main)

	api.replace_playlist_tracks(main, [])

	num = 5

	tracks_to_add =	api.get_latest_playlist_tracks(unchanged, num)
	api.add_tracks_at_end_of_playlist(main, tracks_to_add, group_size)

	expected = api.get_track_ids_from_playlist(tracks_to_add)

	tracks = api.get_latest_playlist_tracks(main, num)
	result = api.get_track_ids_from_playlist(tracks)
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
	playlists_handler: api.PlaylistsManager, total: int, limit: int, expected: tuple[int]):

	unchanged = playlists_handler.get_by_id(PlaylistIDs.unchanged)
	unchanged.total_tracks = total
	gen = api.get_playlist_track_generator(unchanged, limit=limit)

	for i, items in enumerate(gen):
		assert len(items) == expected[i]
		if i == 3:
			break
