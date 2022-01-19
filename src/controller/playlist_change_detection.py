from src.helpers.myers import myers_diff, Keep, Insert, Remove
from src.helpers.data_types import SpotifyPlaylistType

from src.api_handler import sp
from src.api_handler.tracks import Tracks

from src import db


def has_playlist_changed(playlist: SpotifyPlaylistType):
	current_snapshot = playlist.snapshot_id
	previous_snapshot = db.playlists.get_playlist_snapshot_id(playlist.id)
	return previous_snapshot != current_snapshot

def changed_playlists() -> list[SpotifyPlaylistType]:
	playlists = sp.get_all_playlists()
	changed: list[SpotifyPlaylistType] = []
	for playlist in playlists:
		if has_playlist_changed(playlist):
			changed.append(playlist)

	return changed






def calculate_diff(playlist_id: str):
	prev_track_list = db.playlists.get_track_ids(playlist_id)
	curr_track_list_gen = sp.get_playlist_tracks_generator(playlist_id)
	curr_track_list = []

	for tracks in curr_track_list_gen:
		curr_track_list = tracks + curr_track_list

	curr_track_list = Tracks.get_ids(curr_track_list)

	diff = myers_diff(prev_track_list, curr_track_list)
	for elem in diff:
		if isinstance(elem, Keep):
			print(' ' + elem.line)
		elif isinstance(elem, Insert):
			print('+' + elem.line)
		elif isinstance(elem, Remove):
			print('-' + elem.line)


def update_playlist(playlist: SpotifyPlaylistType):
	playlist = db.playlists.get_playlist(playlist.id)
	db.playlists.update_playlist(playlist)
	


def update_all_playlists(playlists: list[SpotifyPlaylistType]):
	for playlist in playlists:
		update_playlist(playlist)
