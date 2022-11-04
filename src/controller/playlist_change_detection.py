from src import db
from src.controller import Diff
from src.api.playlists import PlaylistHandler
from src.helpers.helpers import lookahead
from src.helpers.logger import log
from src.helpers.myers import Myers
from src.types.playlists import PlaylistTrackItem, PlaylistType


def has_playlist_changed(playlist: PlaylistType):
	""" check if current snapshot_id and db snapshot_id are different """
	current_snapshot = playlist.snapshot_id
	previous_snapshot = db.playlists.get_playlist_snapshot_id(playlist.id)
	return previous_snapshot != current_snapshot


def get_changed_playlists(playlists: list[PlaylistHandler]):
	""" filteres the playlists param and returns only
		playlists that changed """
	return [p for p in playlists if has_playlist_changed(p.data)]


def get_playlist_diff(playlist: PlaylistHandler) -> Diff:
	""" returns the difference between tracks in db and on spotify

	requires playlist to exist in database,
	raises PlaylistNotFoundError if not found
	"""

	db_track_list = db.playlists.get_track_ids(playlist.id)
	saved_items: list[PlaylistTrackItem] = []

	myers = Myers(db_track_list)
	gen = playlist.get_track_generator()
	for tracks, has_next in lookahead(gen):
		saved_items = tracks + saved_items

		track_ids = [item.track.id for item in saved_items]
		myers = Myers(db_track_list, track_ids)

		fki = myers.first_keep_index if has_next else 0
		if fki is not None:  # check to save on iterations

			estimated_total = fki + len(saved_items)
			if estimated_total == playlist.total_tracks:
				myers.separate_operations(fki)
				break

			elif not has_next:
				log.error('Something is severly wrong here')
				log.error(f'{db_track_list = }')
				log.error(f'{saved_items = }')

	lookup_table = {item.track.id: item for item in saved_items if item}
	inserts = [lookup_table[line] for line in myers.inserts]

	return Diff(inserts, myers.removals)
