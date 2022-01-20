# from src import api_handler
from src.helpers.myers import Myers, myers_diff, Keep, Insert, Remove
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


def calculate_diff(playlist_id: str, num_tracks: int):
	db_track_list = db.playlists.get_track_names(playlist_id)
	# prev_track_list = db.playlists.get_track_ids(playlist_id)
	sp_track_list_gen = sp.get_playlist_tracks_generator(playlist_id)
	sp_track_list = []

	for tracks in sp_track_list_gen:
		sp_track_list = Tracks.get_names(tracks) + sp_track_list
		myers = Myers(db_track_list, sp_track_list)
		myers.print_diff()
		if myers.has_something(Keep):
			for i, elem in enumerate(myers.diff):
				if isinstance(elem, Keep):
					first_line = elem.line
					break
			index_in_a_list = db_track_list.index(first_line)
			total_tracks_after = i + index_in_a_list + len(sp_track_list)
			if total_tracks_after == num_tracks:
				break



	# curr_track_list = Tracks.get_ids(curr_track_list)

	myers = Myers(db_track_list, sp_track_list)
	for elem in myers.diff:
		if isinstance(elem, Keep):
			print(' ' + elem.line)
		elif isinstance(elem, Insert):
			print('+' + elem.line)
		elif isinstance(elem, Remove):
			print('-' + elem.line)

	print(num_tracks, myers.get_num_elems_after)


def update_playlist(playlist_id: str):
	# playlist = db.playlists.get_playlist(playlist.id)
	playlist = sp.get_one_playlist(playlist_id)
	# db.playlists.update_playlist(playlist)

	calculate_diff(playlist.id, playlist.tracks.total)
	


def update_all_playlists(playlists: list[SpotifyPlaylistType]):
	for playlist in playlists:
		update_playlist(playlist)
