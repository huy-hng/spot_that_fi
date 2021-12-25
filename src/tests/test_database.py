import glob 
import json

from src.database import db_helpers, db_tracks, db_playlists, Session
from src.database.tables import PlaylistTracksAssociation


def check_track_in_playlist():
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	track_id = '14fIlfcmFPlj4V2IazeJ25'
	# track_id = 'asd14fIlfcmFPlj4V2IazeJ25'
	res = db_helpers.is_track_in_playlist(playlist_id, track_id)
	print(res)


def add_playlists():
	with open('./data/playlists.json') as f:
		playlists = json.loads(f.read())
	db_playlists.add_playlists(playlists)


def add_liked_tracks():
	with open(f'./data/liked_tracks.json') as f:
		tracks = json.load(f)
	db_tracks.add_tracks(tracks, liked=True)


def add_tracks_to_playlist(playlist_id: str, tracks: list[dict]):
	db_playlists.add_tracks_to_playlist(playlist_id, tracks)


def add_tracks_to_all_playlists():
	playlist_ids = db_playlists.get_playlists()	

	for playlist_id in playlist_ids:
		with open(f'./data/playlists/{playlist_id}.json') as f:
			tracks = json.load(f)
			add_tracks_to_playlist(playlist_id, tracks)


def liked_tracks_not_in_playlists():
	track_ids = db_tracks.get_liked_tracks_not_in_playlists()

	with Session.begin() as session:
		for track_id in track_ids:
			row = db_tracks.get_track(session, track_id)
			print(row.name)


def get_playlist_tracks(playlist_name: str):
	with Session.begin() as session:
		playlist = db_playlists.get_playlist(session, playlist_name)
		associations: list[PlaylistTracksAssociation] = playlist.tracks
		associations.sort(key=lambda x: x.added_at)
		# sorted(associations/, )

		for ass in associations:
			print(ass.track.name)



	