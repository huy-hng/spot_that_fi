import pytest

from src.api_handler import sp
from src.controller import update_db
from src import api_handler as api
from src.features import update_snippets
from src.tests import PlaylistIDs, TrackIDs

SKIP_SANITY = True

def _replace_unchanged_playlist_with_calm():
	gen = sp.get_playlist_tracks_generator(PlaylistIDs.calm)
	for items in gen:
		sp.replace_playlist_tracks(PlaylistIDs.unchanged, items.track_ids)
		break

def reset_playlists():
	gen = sp.get_playlist_tracks_generator(PlaylistIDs.unchanged)
	for items in gen:
		sp.replace_playlist_tracks(PlaylistIDs.main, items.track_ids)
		break
	empty_snippets_playlist()


def empty_snippets_playlist():
	sp.replace_playlist_tracks(PlaylistIDs.snippet, [])


# @pytest.mark.skip
def test_snippets_from_empty():
	# gather data
	main = sp.get_one_playlist(PlaylistIDs.main)
	snippet = sp.get_one_playlist(PlaylistIDs.snippet)

	# setup
	empty_snippets_playlist()
	update_db.update_playlist_tracks_in_db(main)
	update_db.update_playlist_tracks_in_db(snippet)

	# actual test
	update_snippets.sync_playlist_pair(main, snippet, snippet_size=10)

	tracks = next(sp.get_playlist_tracks_generator(snippet.id))
	assert tracks.track_ids == TrackIDs.unchanged_track_ids[-10:]

def test_mini():
	main = sp.get_one_playlist(PlaylistIDs.main)
	tracks = []
	for i, items in enumerate(sp.get_playlist_tracks_generator(main.id, limit=10)):
		tracks += items.items_
		print(i)

	print(len(tracks))


@pytest.mark.skipif(SKIP_SANITY, reason='Too expensive to run each time.')	
def test_sanity_checks():
	gen = sp.get_playlist_tracks_generator(PlaylistIDs.unchanged)
	items = next(gen)

	assert items.track_ids == TrackIDs.unchanged_track_ids
