from src.api_handler import sp
from src.api_handler.tracks import Tracks

def reset_playlists():
	playlist_id = '6LB26f7o7YcANtlVuxhXZq'
	gen = sp.get_playlist_tracks_generator(playlist_id)

	id = '6BDxVpN7v1HFSRGgt8LYCn'
	for tracks in gen:
		track_ids = Tracks.get_ids(tracks)
		sp.replace_playlist_tracks(id, track_ids)
		break
