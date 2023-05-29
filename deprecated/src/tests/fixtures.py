import shutil
import json

import pytest

from src.api.playlists import PlaylistsHandler
from src.db.initializer import configure_db, delete_tables, get_testing_engine
from src.tests import PlaylistIDs
from src.types.playlists import PlaylistType


@pytest.fixture
def liked_db():
	src = f'./database/test_databases/liked_tracks.db'
	dst = f'./database/Testing.db'
	shutil.copyfile(src, dst)


@pytest.fixture
def empty_db():
	delete_tables()


@pytest.fixture(scope='session')
def init_db():
	engine = get_testing_engine()
	configure_db(engine)


@pytest.fixture(scope='session')
def playlists_handler():
	with open('./data/api_data/current_user_playlist_items.json') as f:
		data: list[dict] = json.load(f)

	playlists = [PlaylistType(p) for p in data]
	playlists = PlaylistsHandler(playlists)
	return playlists


@pytest.fixture(scope='session')
def main(playlists_handler: PlaylistsHandler):
	return playlists_handler.get_by_id(PlaylistIDs.main)


@pytest.fixture(scope='session')
def unchanged(playlists_handler: PlaylistsHandler):
	return playlists_handler.get_by_id(PlaylistIDs.main)


# def replace_tracks(playlist_name: str, track_ids: list[str]):
# 	playlists = LivePlaylists()
# 	playlist = playlists.get_by_name(playlist_name)
# 	playlist.replace_tracks(track_ids)


# @pytest.fixture
# def reset_playlists():
# 	# yield
# 	playlists = LivePlaylists()
# 	playlist = playlists.get_by_name('Playlist')
# 	archive_playlist = playlists.get_by_name('Playlist Archive')

# 	calm = playlists.get_by_name('Calm')
# 	tracks = calm.get_latest_tracks(51)
# 	track_ids = Tracks.get_ids(tracks)

# 	playlist.replace_tracks(track_ids)
# 	archive_playlist.replace_tracks([])
# 	return


# def get_track_ids():
# 	""" get ids for testing """
# 	playlists = LivePlaylists()
# 	calm = playlists.get_by_name('Calm All')

# 	tracks = calm.get_latest_tracks(55)
# 	tracks.reverse()
# 	return Tracks.get_ids(tracks)
