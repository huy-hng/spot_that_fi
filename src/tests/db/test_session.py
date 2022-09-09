from src.db import create_session
import timeit
from src import db
from src.db.tables import PlaylistTable
from src.api.playlists import PlaylistHandler


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


def test_time():
	# result = timeit.timeit(timer)
	# print(result)
	playlist_id = '063Tra4gBrn9kOf0kZQiIT'
	create_stmt = f'created_session("{playlist_id}")'
	create_setup = 'from src.tests.db.test_session import created_session'

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


def created_session(playlist_id: str):
	with create_session() as session:
		playlist = session.query(PlaylistTable).get(playlist_id)


def passed_session(session, playlist_id: str):
	playlist = session.query(PlaylistTable).get(playlist_id)
