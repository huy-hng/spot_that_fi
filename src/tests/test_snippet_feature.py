from src.api_handler import sp
from src.api_handler.tracks import Tracks

unchanged_playlist_id = '6BDxVpN7v1HFSRGgt8LYCn'
calm_playlist_id = '6LB26f7o7YcANtlVuxhXZq'

main_playlist_id = '063Tra4gBrn9kOf0kZQiIT'
snippet_playlist_id = '4gsOp2FJy4lTKrkZronuih'

def replace_unchanged_playlist_with_calm():
	gen = sp.get_playlist_tracks_generator(calm_playlist_id)
	for tracks in gen:
		track_ids = Tracks.get_ids(tracks)
		sp.replace_playlist_tracks(unchanged_playlist_id, track_ids)
		break

def reset_playlists():
	gen = sp.get_playlist_tracks_generator(unchanged_playlist_id)
	for tracks in gen:
		track_ids = Tracks.get_ids(tracks)
		sp.replace_playlist_tracks(main_playlist_id, track_ids)


def empty_snippets_playlist():
	sp.replace_playlist_tracks(snippet_playlist_id, [])

def test_snippets_from_empty():
	empty_snippets_playlist()
	
