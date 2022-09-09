from src import db
from src.db import create_session
from src.db.helpers import does_exist
from src.db.tables import TrackTable
from src.tests import mock_api


def test_add_liked_tracks():
	for items in mock_api.get_liked_tracks_generator():
		db.tracks.like_tracks(items.items)


def test_get_liked_tracks():
	ids = db.tracks.get_liked_tracks()
	assert len(ids) == 3854


def test_get_liked_track():
	track_id = '6Lt7kRIl2Sw9gJtwaTTWZ2'
	with create_session() as session:
		q = session.query(TrackTable).filter(TrackTable.liked.has())
		print(does_exist(q))
		liked = db.tracks.get_liked_track(track_id, session=session)
		r = liked.track.liked.track.duration_ms
		print(r)


def test_unlike_tracks():
	for items in mock_api.get_liked_tracks_generator():
		ids = [track.id for track in items.tracks]
		db.tracks.unlike_tracks(ids)


""" deprecated """


def liked_tracks_not_in_playlists():
	track_ids = db.tracks.get_liked_tracks_not_in_playlists()

	for track_id in track_ids:
		row = db.tracks.get_track(track_id)
		print(row.name)
