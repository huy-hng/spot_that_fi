from helpers.myers import myers_diff
from helpers.data_types import SpotifyPlaylistType

from src.api_handler import sp

import db


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

	while True:
		curr_track_list = curr_track_list_gen.next() + curr_track_list

	# diff = myers_diff(prev_track_list, curr_track_list)


def update_playlist(playlist: SpotifyPlaylistType):
	db.playlists.update_playlist_snapshot()


def update_all_playlists(playlists: list[SpotifyPlaylistType]):
	for playlist in playlists:
		update_playlist(playlist)
