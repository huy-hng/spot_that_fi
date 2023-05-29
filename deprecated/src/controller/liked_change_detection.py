from difflib import SequenceMatcher
from typing import Generator, NamedTuple

from src import db
from src.controller import Diff
from src.helpers.helpers import lookahead, timer
from src.helpers.logger import log
from src.helpers.myers import Myers, Operations
from src.helpers.sequencer import Sequencer
from src.tests import mock_api as api
from src.types.tracks import LikedTrackItem, LikedTrackList


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
	- so if there are no new insertions and the total is the same, nothing changed

	"""
	items = next(api.get_liked_tracks_generator())
	prev_total = db.tracks.get_len_liked()
	curr_total = items.total
	if prev_total != curr_total:
		return True


def has_equal(ops: list[tuple[str, int, int, int, int]]):
	for tag, _, _, _, _ in ops:
		if tag == 'equal':
			return True
	return False


@timer
def get_diff(track_generator: Generator[LikedTrackList, None, None]) -> Diff[LikedTrackItem]:
	"""
	1. check if total liked tracks is different
	2. do myers with keep first algorithm
	"""
	if track_generator is None:
		track_generator = api.get_liked_tracks_generator()

	log.info('Getting Liked Tracks Diff')

	db_ids = db.tracks.get_liked_tracks()
	len_db = db.tracks.get_len_liked()
	log.debug(f'{len_db=}')
	saved_items: list[LikedTrackItem] = []

	s = SequenceMatcher(None, db_ids)
	inserts: list[LikedTrackItem] = []
	removals: list[str] = []
	inserts2 = []

	all_inserts_found = False
	expected_deletes = 0

	for items_list, has_next in lookahead(track_generator):
		saved_items += items_list.items
		saved_items.sort(key=lambda x: (x.added_at, x.track.id), reverse=True)
		track_ids = [item.track.id for item in saved_items]

		s.set_seq2(track_ids)

		log.debug(f'{len(track_ids)=}')
		ops = s.get_opcodes()

		if not has_equal(ops):
			continue

		if has_next:
			del ops[-1]
		else:
			log.debug('Iterated through all liked tracks on spotify.')

		for tag, i1, i2, j1, j2 in ops:
			if tag == 'insert':
				inserts = saved_items[j1:j2]
				inserts2 = track_ids[j1:j2]
			if tag == 'delete':
				removals += db_ids[i1:i2]
			# log.debug('{:7}   a[{}:{}] --> b[{}:{}]'.format(tag, i1, i2, j1, j2))


		if not all_inserts_found:
			# for debugging and checking correctness
			log.debug(f'{len(inserts)} inserts found.')
			# log.debug('All inserts found.')
			all_inserts_found = True
			log.debug(items_list.total)
			expected_changes: int = items_list.total - len_db
			expected_deletes = abs(expected_changes - len(inserts))
			log.debug(f'Expecting {expected_changes} changes.')
			log.debug(f'Looking for {expected_deletes} removals.')

		if expected_deletes == len(removals):
			break

		# log.debug('====================')
		log.debug(f'{len(removals)} removals found so far.')

		removals = [] # reset removals since it gets appended

	log.debug(f'{len(removals)} removals found.')
	return Diff(inserts, removals)


def get_diff_old() -> Diff:
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
