from pprint import pprint
from typing import NamedTuple

from src import db
from src.helpers.helpers import lookahead, timer
from src.helpers.logger import log
from src.helpers.myers import Myers
from src.tests import mock_api as api
from src.types.tracks import LikedTrackItem


def has_liked_tracks_changed():
	""" 
	liked track generator returns tracks sorted by added_at
	the first item has been liked most recently

	keep in mind:
	- new liked tracks are always first
	- tracks cant switch places, except:
	- if a liked track gets unliked and liked again the total will stay the same
		but theres one new insertion
		this can be accounted for by checking if the inserted songs are in the db
		if yes then it has been unliked and reliked
	- so if there are not new insertions and total is the same, nothing changed

	"""
	items = next(api.get_liked_tracks_generator())
	prev_total = db.tracks.get_len_liked()
	curr_total = items.total
	if prev_total != curr_total:
		return True




class Diff(NamedTuple):
	inserts: list[LikedTrackItem] = []
	removals: list[str] = []

@timer
def get_diff() -> Diff:
	"""
	1. check if total liked tracks is different
	2. do myers with keep first algorithm
	"""
	# REFACTOR: merge with playlist change detector
	db_ids = db.tracks.get_liked_tracks()
	len_db = db.tracks.get_len_liked()
	saved_items: list[LikedTrackItem] = []

	myers = Myers([''])
	gen = api.get_liked_tracks_generator()
	for items_list, has_next in lookahead(gen):
		saved_items += items_list.items

		track_ids = [item.track.id for item in saved_items]
		new_len = len(track_ids)
		myers = Myers(db_ids[:new_len], track_ids)

		fki = myers.last_keep_index if has_next else 0
		if fki is not None:  # check to save on iterations
			# fki = items_list.total - fki
			estimated_total = fki + (len_db - len(myers.removals))
			if estimated_total == items_list.total:
				myers.separate_operations(fki)
				break

			# elif not has_next:
				# log.error('Something is severly wrong here')
				# log.error(f'{db_ids = }')
				# log.error(f'{saved_items = }')

	lookup_table = {item.track.id: item for item in saved_items if item}
	inserts = [lookup_table[line] for line in myers.inserts]

	return Diff(inserts, myers.removals)
