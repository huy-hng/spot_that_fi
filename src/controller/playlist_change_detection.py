from typing import NamedTuple
from src.helpers.myers import Myers, Operations
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


class Diff(NamedTuple):
	inserts: list[PlaylistTracksItem] = []
	removals: list[PlaylistTracksItem] = []

def get_track_diff(playlist: AllPlaylists | SinglePlaylist) -> Diff:
	db_track_list = db.playlists.get_track_ids(playlist.id)
	sp_track_list: dict[str, PlaylistTracksItem] = {}

	myers = Myers()
	# TEST changes
	for tracks in sp.get_playlist_tracks_generator(playlist.id):
		sp_track_list.update({item.track.id: item for item in tracks.items_})

		track_ids = tracks.track_ids
		myers = Myers(db_track_list, track_ids)

		# if myers.index_of_first_keep is not None:
		if myers.keeps:
			first_keep = myers.keeps[0]

			index_in_db_list = db_track_list.index(first_keep)
			total_tracks_after = index_in_db_list + len(track_ids)
			if total_tracks_after == playlist.tracks.total:
				myers.print_diff()
				break

	inserts = [sp_track_list[line] for line in myers.inserts]
	removals = [sp_track_list[line] for line in myers.removals]

	return Diff(inserts, removals)
