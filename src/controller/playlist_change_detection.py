from src.helpers.myers import Myers, myers_diff, Keep, Insert, Remove
from src.helpers.data_types import SpotifyPlaylistType

from src.api_handler import sp
from src.api_handler.tracks import Tracks

from src import db


def has_playlist_changed(playlist: SpotifyPlaylistType):
	""" check if current snapshot_id and db snapshot_id are different """
	current_snapshot = playlist.snapshot_id
	previous_snapshot = db.playlists.get_playlist_snapshot_id(playlist.id)
	return previous_snapshot != current_snapshot


def changed_playlists(playlists: list[SpotifyPlaylistType]):
	""" filteres the playlists param and returns only
			playlists that changed """

	changed: list[SpotifyPlaylistType] = []
	for playlist in playlists:
		if has_playlist_changed(playlist):
			changed.append(playlist)

	return changed


def calculate_diff(playlist_id: str, num_tracks: int):
	""" returns a tuple where the first value is removals 
			and second is inserts """
	
	db_track_list = db.playlists.get_track_ids(playlist_id)
	# prev_track_list = db.playlists.get_track_ids(playlist_id)
	sp_track_list_gen = sp.get_playlist_tracks_generator(playlist_id)
	sp_track_list = {}
	track_ids = []

	for tracks in sp_track_list_gen:
		sp_track_list.update({track['track']['id']: track for track in tracks})
		track_ids = Tracks.get_ids(tracks) + track_ids

		myers = Myers(db_track_list, track_ids)
		index_first_keep = myers.index_of_first_keep
		if index_first_keep is not None:
			first_keep = myers.diff[index_first_keep].line

			index_in_db_list = db_track_list.index(first_keep)
			total_tracks_after = index_in_db_list + len(track_ids)
			if total_tracks_after == num_tracks:
				myers.print_diff(print)
				break

	inserts = []
	removals = []
	for elem in myers.diff[myers.index_of_first_keep:]:
		if isinstance(elem, Insert):
			track = sp_track_list.get(elem.line)
			inserts.append(track)
		elif isinstance(elem, Remove):
			removals.append(elem.line)

	return removals, inserts
