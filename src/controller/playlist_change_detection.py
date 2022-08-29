from src.helpers.myers import Myers, Keep, Insert, Remove
from src.types.playlists import AllPlaylists, PlaylistTracksItem, SinglePlaylist, AbstractPlaylistType
from src.api_handler import sp

from src import db


def has_playlist_changed(playlist: AllPlaylists | SinglePlaylist):
	""" check if current snapshot_id and db snapshot_id are different """
	current_snapshot = playlist.snapshot_id
	previous_snapshot = db.playlists.get_playlist_snapshot_id(playlist.id)
	return previous_snapshot != current_snapshot


def get_changed_playlists(playlists: list[AllPlaylists]):
	""" filteres the playlists param and returns only
		playlists that changed """
	return [p for p in playlists if has_playlist_changed(p)]


def get_track_diff(playlist_id: str, num_tracks: int):
	""" returns a tuple where the first value is removals 
			and second is inserts """
	
	db_track_list = db.playlists.get_track_ids(playlist_id)
	sp_track_list: dict[str, PlaylistTracksItem] = {}

	myers = None
	# TEST changes
	for playlist_tracks in sp.get_playlist_tracks_generator(playlist_id):
		track_ids = playlist_tracks.track_ids

		# REFACTOR: seems a little unelegant
		sp_track_list.update(
			{item.track.id: item for item in playlist_tracks.items_}
		)

		myers = Myers(db_track_list, track_ids)
		index_first_keep = myers.index_of_first_keep
		if index_first_keep is not None:
			first_keep = myers.diff[index_first_keep].line

			index_in_db_list = db_track_list.index(first_keep)
			total_tracks_after = index_in_db_list + len(track_ids)
			if total_tracks_after == num_tracks:
				myers.print_diff(print)
				break

	inserts: list[PlaylistTracksItem] = []
	removals: list[PlaylistTracksItem] = []

	if myers is None:
		return removals, inserts

	for elem in myers.diff[myers.index_of_first_keep:]:
		if isinstance(elem, Insert):
			track = sp_track_list.get(elem.line)
			if track is not None:
				inserts.append(track)
		elif isinstance(elem, Remove):
			removals.append(elem.line)

	return removals, inserts
