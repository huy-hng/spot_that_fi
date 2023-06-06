from src import api, db
from src.behaviors import Diff
from src.utils import lookahead
from src import exceptions

from src import log
from src.utils.myers import Myers
from src import types


def update_playlist_tracks_in_db(playlist: types.PlaylistType, diff: Diff | None=None):
	""" playlist should be very up to date """
	# TEST: check if this function works for an empty playlist that has just been added

	if not has_playlist_changed(playlist): return

	db.playlists.update_playlist(playlist)

	if diff is None:
		diff = get_playlist_diff(playlist)

	db.playlists.remove_tracks_from_playlist(playlist.id, diff.removals)
	db.playlists.add_tracks_to_playlist(playlist.id, diff.inserts)
	return diff


def update_all_playlist_tracks_in_db():
	playlists = api.PlaylistsManager()
	for playlist in playlists.playlists:
		update_playlist_tracks_in_db(playlist)


def has_playlist_changed(playlist: types.PlaylistType):
	'''
	check if current snapshot_id and db snapshot_id are different
	'''
	current_snapshot = playlist.snapshot_id
	previous_snapshot = db.playlists.get_playlist_snapshot_id(playlist.id)
	return previous_snapshot != current_snapshot


def get_changed_playlists(playlists: list[types.PlaylistType]):
	'''
	filteres the playlists param and returns only playlists that changed
	'''
	return [p for p in playlists if has_playlist_changed(p)]



def get_playlist_diff(playlist: types.PlaylistType) -> Diff[types.PlaylistTrackItem]:
	'''
	returns the difference between tracks in db and on spotify

	requires playlist to exist in database,
	raises PlaylistNotFoundError if not found
	'''

	try:
		db_track_list = db.playlists.get_track_ids(playlist.id)
	except exceptions.PlaylistNotFoundError:
		db_track_list = []

	saved_items: list[types.PlaylistTrackItem] = []

	myers = Myers(db_track_list)
	gen = api.get_playlist_track_generator(playlist)
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
