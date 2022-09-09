import dataclasses
import json

import pytest
from src import db
from src.api.playlists import PlaylistHandler, PlaylistsHandler, get_names
from src.controller import playlist_change_detection as pcd
from src.db import create_session
from src.tests import PlaylistIDs
from src.types.playlists import PlaylistTrackItem, PlaylistType


@pytest.mark.skip
def test_get_track_diff(playlists_handler: PlaylistsHandler):
	# snippet = sp.get_one_playlist(PlaylistIDs.snippet)
	snippet = playlists_handler.get_by_id(PlaylistIDs.snippet)
	diff = pcd.get_playlist_diff(snippet)
	# removals = PlaylistHandler.get_names(diff.removals)
	inserts = get_names(diff.inserts)
	print(diff.removals)
	print(inserts)


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


def test_add_playlists(playlists_handler: PlaylistsHandler):
	playlists = [playlist.data for playlist in playlists_handler.playlists]
	db.playlists.add_playlists(playlists)

	ids = db.playlists.get_playlist_ids()
	print(ids)
	return ids


def test_playlist_update(main: PlaylistHandler):
	with create_session() as session:
		# setup (change snapshot id)
		cp = dataclasses.asdict(main.data)
		cp['snapshot_id'] = 'asdfasdf'
		cp = PlaylistType(cp)
		db.playlists.update_playlist(cp)

		# actual test
		db_playlist = db.playlists.get_playlist(main.id, session=session)
		old_snapshot = db_playlist.snapshot_id

		db.playlists.update_playlist(main.data)

		db_playlist = db.playlists.get_playlist(main.id, session=session)
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


def get_playlist_tracks(playlist_name: str):
	playlist_id = db.playlists.get_id_from_name(playlist_name)
	playlist = db.playlists.get_playlist(playlist_id)
	associations: list[db.tables.PlaylistAssociation] = playlist.tracks
	associations.sort(key=lambda x: x.added_at)
	# sorted(associations/, )

	for ass in associations:
		print(ass.track.name)
