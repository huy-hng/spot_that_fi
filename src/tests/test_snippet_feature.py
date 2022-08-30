from src.api_handler import sp
from src.features import update_snippets
from src.tests import PlaylistIDs

def _replace_unchanged_playlist_with_calm():
	gen = sp.get_playlist_tracks_generator(PlaylistIDs.calm)
	for items in gen:
		sp.replace_playlist_tracks(PlaylistIDs.unchanged, items.track_ids)
		break

def reset_playlists():
	gen = sp.get_playlist_tracks_generator(PlaylistIDs.unchanged)
	for items in gen:
		sp.replace_playlist_tracks(PlaylistIDs.main, items.track_ids)


def empty_snippets_playlist():
	sp.replace_playlist_tracks(PlaylistIDs.snippet, [])


def _test_snippets_from_empty():
	empty_snippets_playlist()
	update_snippets.sync_all_playlists()

	
