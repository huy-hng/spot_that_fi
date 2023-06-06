from difflib import SequenceMatcher
from typing import Generator

from src import api, db, log
from src.behaviors import Diff
from src.utils import lookahead
from src import types


def update_db_liked_tracks():
	gen = api.get_liked_tracks_generator()
	diff = get_diff(gen)
	db.tracks.like_tracks(diff.inserts)
	db.tracks.unlike_tracks(diff.removals)


def has_liked_tracks_changed():
	'''
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
	'''
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


def get_diff(track_generator: Generator[types.LikedTrackList, None, None]) -> Diff[types.LikedTrackItem]:
	'''
	1. check if total liked tracks is different
	2. do myers with keep first algorithm
	'''
	if track_generator is None:
		track_generator = api.get_liked_tracks_generator()

	log.info('Getting Liked Tracks Diff')

	db_ids = db.tracks.get_liked_tracks()
	len_db = db.tracks.get_len_liked()
	log.debug(f'{len_db=}')
	saved_items: list[types.LikedTrackItem] = []

	s = SequenceMatcher(None, db_ids)
	inserts: list[types.LikedTrackItem] = []
	removals: list[str] = []

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
			if tag == 'delete':
				removals += db_ids[i1:i2]

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
