import pytest

from src import api
from src.api import PlaylistHandler
from src.controller import update_db
from src.features import update_snippets
from src.tests import PlaylistIDs, TrackIDs

SKIP_SANITY = True


def _replace_unchanged_playlist_with_calm():
	gen = api.get_playlist_tracks_generator(PlaylistIDs.calm)
	for items in gen:
		api.replace_playlist_tracks(
			PlaylistIDs.unchanged, PlaylistHandler.get_ids(items.items_))
		break


def reset_playlists():
	gen = api.get_playlist_tracks_generator(PlaylistIDs.unchanged)
	for items in gen:
		api.replace_playlist_tracks(
			PlaylistIDs.main, PlaylistHandler.get_ids(items.items_))
		break
	empty_snippets_playlist()


def empty_snippets_playlist():
	api.replace_playlist_tracks(PlaylistIDs.snippet, [])


# @pytest.mark.skip
def test_snippets_from_empty():
	# gather data
	main = api.get_one_playlist(PlaylistIDs.main)
	snippet = api.get_one_playlist(PlaylistIDs.snippet)

	# setup
	empty_snippets_playlist()
	update_db.update_playlist_tracks_in_db(main)
	update_db.update_playlist_tracks_in_db(snippet)

	# actual test
	update_snippets.sync_playlist_pair(main, snippet, snippet_size=10)

	tracks = next(api.get_playlist_tracks_generator(snippet.id))
	assert PlaylistHandler.get_ids(
		tracks.items_) == TrackIDs.unchanged_track_ids[-10:]


def test_mini():
	main = api.get_one_playlist(PlaylistIDs.main)
	tracks = []
	for i, items in enumerate(api.get_playlist_tracks_generator(main.id, limit=10)):
		tracks += items.items_
		print(i)

	print(len(tracks))


@pytest.mark.skipif(SKIP_SANITY, reason='Too expensive to run each time.')
def test_sanity_checks():
	gen = api.get_playlist_tracks_generator(PlaylistIDs.unchanged)
	items = next(gen)

	assert PlaylistHandler.get_ids(items.items_) == TrackIDs.unchanged_track_ids
