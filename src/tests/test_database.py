import dataclasses
import json

import pytest
from src import db
from src.api.playlists import PlaylistHandler, PlaylistsHandler, get_names
from src.controller import playlist_change_detection as pcd
from src.db import create_session
from src.tests import PlaylistIDs
from src.types.playlists import PlaylistType


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
		db.playlists._update_playlist(session, cp)

		# actual test
		db_playlist = db.playlists._get_playlist(session, main.id)
		old_snapshot = db_playlist.snapshot_id

		db.playlists._update_playlist(session, main.playlist_data)

		db_playlist = db.playlists._get_playlist(session, main.id)
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


def check_track_in_playlist():
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	track_id = '14fIlfcmFPlj4V2IazeJ25'
	# track_id = 'asd14fIlfcmFPlj4V2IazeJ25'
	res = db.helpers.is_track_in_playlist(playlist_id, track_id)
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
		playlist = db.playlists._get_playlist(session, playlist_id)
		associations: list[db.tables.PlaylistTracksAssociation] = playlist.playlist_track_association
		associations.sort(key=lambda x: x.added_at)
		# sorted(associations/, )

		for ass in associations:
			print(ass.track.name)
