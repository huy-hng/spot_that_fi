import dataclasses
import json
import time
import timeit

import pytest
from src import api, db
from src.api.playlists import PlaylistHandler, PlaylistsHandler, get_names
from src.controller import playlist_change_detection as pcd
from src.db import create_session
from src.db.tables import LikedTable, TrackTable
from src.db.helpers import does_exist
from src.helpers.exceptions import PlaylistNotFoundError
from src.helpers.helpers import write_data
from src.tests import PlaylistIDs
from src.tests import mock_api
from src.types.playlists import PlaylistTrackItem, PlaylistType
from src.types.tracks import LikedTrackList

# TODO: sample data for testing that stays the same


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


def test_add_playlists(playlists_handler: PlaylistsHandler):
	playlists = [playlist.data for playlist in playlists_handler.playlists]
	db.playlists.add_playlists(playlists)

	ids = db.playlists.get_playlist_ids()
	print(ids)
	return ids


def test_add_playlist_tracks(playlists_handler: PlaylistsHandler):
	playlist_ids = test_add_playlists(playlists_handler)

	for playlist_id in playlist_ids:
		try:
			with open(f'./data/playlists/{playlist_id}.json') as f:
				tracks_data = json.load(f)
		except Exception:
			continue

		tracks = [PlaylistTrackItem(data) for data in tracks_data]
		db.playlists.add_tracks_to_playlist(playlist_id, tracks)
		break

	for id in playlist_ids:
		names = db.playlists.get_track_names(id)
		print(len(names))
		break


def test_session(unchanged: PlaylistHandler):

	playlist = unchanged.data
	print(playlist.id)
	playlist.id = 'asdfsdf'
	playlist.name = 'ergdf'

	# res = db.playlists.nested_session(playlist)
	# print(res)

	db.playlists.delete_playlist(playlist.id)
	ids = db.playlists.get_playlist_ids()
	assert playlist.id not in ids

	return []


@pytest.mark.skip
def test_get_track_diff(playlists_handler: PlaylistsHandler):
	# snippet = sp.get_one_playlist(PlaylistIDs.snippet)
	snippet = playlists_handler.get_by_id(PlaylistIDs.snippet)
	diff = pcd.get_playlist_diff(snippet)
	# removals = PlaylistHandler.get_names(diff.removals)
	inserts = get_names(diff.inserts)
	print(diff.removals)
	print(inserts)


def test_playlist_update(main: PlaylistHandler):
	with create_session() as session:
		# setup (change snapshot id)
		cp = dataclasses.asdict(main.data)
		cp['snapshot_id'] = 'asdfasdf'
		cp = PlaylistType(cp)
		db.playlists.update_playlist(session, cp)

		# actual test
		db_playlist = db.playlists.get_playlist(session, main.id)
		old_snapshot = db_playlist.snapshot_id

		db.playlists.update_playlist(session, main.data)

		db_playlist = db.playlists.get_playlist(session, main.id)
		new_snapshot = db_playlist.snapshot_id

		# print(f'{old_snapshot=}')
		# print(f'{new_snapshot=}')
		# print(f'{old_snapshot == new_snapshot=}')
		# print(f'{main.snapshot_id=}')

		assert not old_snapshot == new_snapshot


def get_tracks_in_db_playlist():
	names = db.playlists.get_track_names(PlaylistIDs.snippet)
	for name in names:
		print(name)


def test_check_track_in_playlist(unchanged: PlaylistHandler):
	track_id = '14fIlfcmFPlj4V2IazeJ25'
	ids = db.playlists.get_track_ids(unchanged.id)
	# track_id = 'asd14fIlfcmFPlj4V2IazeJ25'
	res = db.playlists.is_track_in_playlist(unchanged.id, track_id)
	print(res)


def add_playlists():
	with open('./data/playlists.json') as f:
		playlists = json.loads(f.read())
	db.playlists.update_playlists(playlists)


def add_liked_tracks():
	with open(f'./data/liked_tracks.json') as f:
		tracks = json.load(f)
	db.tracks.add_tracks(tracks, liked=True)


def liked_tracks_not_in_playlists():
	track_ids = db.tracks.get_liked_tracks_not_in_playlists()

	for track_id in track_ids:
		row = db.tracks.get_track(track_id)
		print(row.name)


def get_playlist_tracks(playlist_name: str):
	playlist_id = db.playlists.get_id_from_name(playlist_name)
	playlist = db.playlists.get_playlist(playlist_id)
	associations: list[db.tables.PlaylistAssociation] = playlist.tracks
	associations.sort(key=lambda x: x.added_at)
	# sorted(associations/, )

	for ass in associations:
		print(ass.track.name)


def created_session(playlist_id: str):
	with create_session() as session:
		playlist = session.query(db.tables.Playlist).get(playlist_id)


def passed_session(session, playlist_id: str):
	playlist = session.query(db.tables.Playlist).get(playlist_id)


def test_time():
	# result = timeit.timeit(timer)
	# print(result)
	playlist_id = '063Tra4gBrn9kOf0kZQiIT'
	create_stmt = f'created_session("{playlist_id}")'
	create_setup = 'from src.tests.test_database import created_session'

	passed_stmt = f'passed_session(session, "{playlist_id}")'
	passed_setup = """\
from src.tests.test_database import passed_session
from src.db import SessionMaker
session = SessionMaker()
"""
	num = 10000
	passed = timeit.timeit(passed_stmt, passed_setup, number=num)
	created = timeit.timeit(create_stmt, create_setup, number=num)

	print(f'{created=}')
	print(f'{passed=}')
