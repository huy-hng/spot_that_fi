from src import db
from src.db import create_session
from src.db.helpers import does_exist
from src.db.tables import TrackTable, LikedTable
from src.helpers.helpers import timer
from src.tests import mock_api
from src.types.tracks import LikedTrackItem, LikedTrackList, TrackDict
from src.controller import liked_change_detection as lcd


# TODO: remove LikedTable entry and see what happens with TrackTable entry
def test_add_liked_tracks(empty_db):
# def test_add_liked_tracks():
	for items in mock_api.get_liked_tracks_generator():
		db.tracks.like_tracks(items)


# TODO: use different databases to test different things.
# this way things are going to be faster
# ex: a test needs a specific fully populated db, emptying it and populating it
# 	is very expensinve
def test_diff(empty_db):
	# for items in mock_api.get_liked_tracks_generator():
	# 	db.tracks.like_tracks(items)
	# test_add_liked_tracks()
	ids = db.tracks.get_liked_tracks()
	# db.tracks.unlike_tracks(ids[30:70])

	# TODO: something is still wrong with the algorithm. It should only have inserts
	# when tracks are removed with unlike_tracks
	# testing needs to be done with proper data
	# i.e. added and removed data from mock_api
	# this can be achieved by not adding all mock_api data to the db
	# instead leave some out, which are going to be inserts
	# and skip some, which are going to be removals
	diff = lcd.get_diff()
	print(len(diff.inserts))
	print(len(diff.removals))


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
		db.tracks.like_tracks(items)
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
