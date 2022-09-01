from typing import NamedTuple
from src.helpers.helpers import lookahead
from src.helpers.myers import Myers, Operations
from src.types.playlists import AllPlaylists, PlaylistTracksItem, SinglePlaylist, AbstractPlaylistType
from src.api_handler import sp
from src.helpers.logger import log

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
	""" requires playlist to exist in database\n
		raises PlaylistNotFoundError if not found """
	db_track_list = db.playlists.get_track_ids(playlist.id)
	saved_items: list[PlaylistTracksItem] = []

	myers = Myers(db_track_list)
	gen = sp.get_playlist_tracks_generator(playlist.id)
	for tracks, has_next in lookahead(gen):
		saved_items = tracks.items_ + saved_items

		track_ids = [item.track.id for item in saved_items]
		myers = Myers(db_track_list, track_ids)

		fki = myers.first_keep_index if has_next else 0
		if fki is not None: # check to save on iterations

			estimated_total = fki + len(saved_items)
			if estimated_total == playlist.tracks.total:
				myers.separate_operations(fki)
				break

			elif not has_next:
				log.error('Something is severly wrong here')
				log.error(f'{db_track_list = }')
				log.error(f'{saved_items = }')

	lookup_table = {item.track.id: item for item in saved_items}
	inserts = [lookup_table[line] for line in myers.inserts]
	removals = [lookup_table[line] for line in myers.removals]

	return Diff(inserts, removals)
