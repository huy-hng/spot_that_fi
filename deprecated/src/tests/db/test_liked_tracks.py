from src import db
from src.db import create_session
from src.db.helpers import does_exist
from src.db.tables import TrackTable, LikedTable
from src.helpers.helpers import read_data, timer
from src.helpers.myers import Myers, Operations
from src.tests import mock_api
from src.types.tracks import LikedTrackItem, LikedTrackList, TrackDict
from src.controller import liked_change_detection as lcd


def test_add_liked_tracks(empty_db):
# def test_add_liked_tracks():
	for items in mock_api.get_liked_tracks_generator():
		db.tracks.like_tracks(items.items)


def test_data_diff():
	"""
	testing the difference between old and new data
	"""
	old = read_data('testing_data/all_liked_tracks_2022-09-08')
	new = read_data('testing_data/all_liked_tracks_2022-11-04')

	old = [LikedTrackList(d) for d in old]
	new = [LikedTrackList(d) for d in new]

	old_tracks: list[LikedTrackItem] = []
	new_tracks: list[LikedTrackItem] = []

	for item in old:
		old_tracks += item.items
	for item in new:
		new_tracks += item.items

	old_tracks.sort(key=lambda x: (x.added_at, x.track.id), reverse=True)
	new_tracks.sort(key=lambda x: (x.added_at, x.track.id), reverse=True)

	old_tracks_dict = {track.track.id: track for track in old_tracks}
	new_tracks_dict = {track.track.id: track for track in new_tracks}
	# print(new_tracks_dict)


	print(len(old_tracks))
	some_string = 'asdf'
	# some_string.
	old_track_ids = [track.track.id for track in old_tracks]
	new_track_ids = [track.track.id for track in new_tracks]
	myers = Myers(old_track_ids, new_track_ids)
	myers.print_diff()
	for d in myers.diff:
		if d.operation == Operations.:
			...
		if d.operation == Operations.Remove:
			o = old_tracks_dict.get(d.line)
			assert o is not None
			print(o.track.id)
			
			# n = new_tracks_dict[d.line]
			# if o is not None:
			# 	print(o.added_at)
			# 	print(n.track.name)
			# print(n.added_at)
			# print()


def test_diff(liked_db):
	# inserts = 0
	# removals = 0
	def get_liked_tracks_generator():
		# data = read_data('testing_data/all_liked_tracks')
		data = read_data('testing_data/all_liked_tracks_2022-11-04')
		# del data[3]
		# del data[5]
		# for d in data:
		# 	d['total'] = d['total'] - removals

		for d in data:
			yield LikedTrackList(d)

	# ids = db.tracks.get_liked_tracks()
	# db.tracks.unlike_tracks(ids[:inserts])

	gen = get_liked_tracks_generator()
	diff = lcd.get_diff(gen)
	print(len(diff.inserts))
	print(len(diff.removals))

	'6vnx0pxiLYsMk7bRMe0TO8'
	'43uAAecpFKIzngplASa9nb'
	'7bFWaXKr9DA5pZioUJzUsg'
	'5VoPWJ85oxMCja2hfIBual'
	'6555WEA9K1U6QwKeSJYf8K'
	# assert len(diff.inserts) == inserts
	# assert len(diff.removals) == removals


@timer
def test_get_sorted_limited():
	with create_session() as session:
		query: list[LikedTable] = session.query(LikedTable).order_by(
			LikedTable._added_at.desc()).limit(50).all()  # type: ignore
		# for q in query:
		# 	print(q.index)


def test_get_liked_ids():
	ids = db.tracks.get_liked_tracks()
	print(ids[0])


def test_get_length():
	len_ids = db.tracks.get_len_liked()
	assert len_ids == 3854


def test_get_one_track():
	track_id = '6Lt7kRIl2Sw9gJtwaTTWZ2'
	with create_session() as session:
		q = session.query(TrackTable).filter(TrackTable.liked.has())
		liked = db.tracks.get_liked_track(track_id, session=session)
		r = liked.track.liked.track.id
		assert r == track_id


def test_unlike_tracks():
	for items in mock_api.get_liked_tracks_generator():
		db.tracks.like_tracks(items.items)
		len_before = db.tracks.get_len_liked()

		ids = [track.id for track in items.tracks]

		db.tracks.unlike_tracks(ids)
		len_after = db.tracks.get_len_liked()
		assert len_before - len_after == len(ids)

		break


""" deprecated """


def liked_tracks_not_in_playlists():
	track_ids = db.tracks.get_liked_tracks_not_in_playlists()

	for track_id in track_ids:
		row = db.tracks.get_track(track_id)
		print(row.name)
