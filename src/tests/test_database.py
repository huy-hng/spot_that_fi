import dataclasses
import json
import time
import timeit

import pytest
from src import db
from src.api.playlists import PlaylistHandler, PlaylistsHandler, get_names
from src.controller import playlist_change_detection as pcd
from src.tests import PlaylistIDs
from src.types.playlists import PlaylistType
from src.helpers.exceptions import PlaylistNotFoundError


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


def test_session(unchanged: PlaylistHandler):

	playlist = unchanged.playlist_data
	print(playlist.id)
	playlist.id = 'asdfsdf'
	playlist.name = 'ergdf'

	# res = db.playlists.nested_session(playlist)
	# print(res)

	db.playlists.delete_playlist(playlist.id)
	ids = db.playlists.get_all_playlists()
	assert playlist.id not in ids
	# db.playlists.nested_session(playlist)
	# db.playlists._get_playlist(playlist.id)

	# db.playlists._delete_playlist(playlist.id)

	# with pytest.raises(PlaylistNotFoundError):
	# 	db.playlists._get_playlist(playlist.id)

	# time.sleep(5)
	# with create_session() as session:
	# 	db.playlists._delete_playlist(session, playlist.id)

	# 	with pytest.raises(PlaylistNotFoundError):
	# 		db.playlists._get_playlist(session, playlist.id)

	# a.close
	# playlist = _get_playlist(a, q[-1].id)
	# print(playlist.id)

	# close_all_sessions()
	# ids = [_get_playlist(sess, playlist.id).id for playlist in q]

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
		cp = dataclasses.asdict(main.playlist_data)
		cp['snapshot_id'] = 'asdfasdf'
		cp = PlaylistType(cp)
		db.playlists.update_playlist(session, cp)

		# actual test
		db_playlist = db.playlists.get_playlist(session, main.id)
		old_snapshot = db_playlist.snapshot_id

		db.playlists.update_playlist(session, main.playlist_data)

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


def add_tracks_to_playlist(playlist_id: str, tracks: list[dict]):
	db.playlists.add_tracks_to_playlist(playlist_id, tracks)


def add_tracks_to_all_playlists():
	playlist_ids = db.playlists.get_all_playlists()

	for playlist_id in playlist_ids:
		with open(f'./data/playlists/{playlist_id}.json') as f:
			tracks = json.load(f)
			add_tracks_to_playlist(playlist_id, tracks)


def liked_tracks_not_in_playlists():
	track_ids = db.tracks.get_liked_tracks_not_in_playlists()

	with create_session() as session:
		for track_id in track_ids:
			row = db.tracks.get_track(session, track_id)
			print(row.name)


def get_playlist_tracks(playlist_name: str):
	with create_session() as session:
		playlist_id = db.playlists.get_id_from_name(playlist_name)
		playlist = db.playlists.get_playlist(session, playlist_id)
		associations: list[db.tables.PlaylistTracksAssociation] = playlist.playlist_track_association
		associations.sort(key=lambda x: x.added_at)
		# sorted(associations/, )

		for ass in associations:
			print(ass.track.name)
