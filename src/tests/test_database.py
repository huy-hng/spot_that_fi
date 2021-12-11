import glob 
import json

from src.database import db_helpers, db_tracks, db_playlists


def check_track_in_playlist():
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	track_id = '14fIlfcmFPlj4V2IazeJ25'
	# track_id = 'asd14fIlfcmFPlj4V2IazeJ25'
	res = db_helpers.is_track_in_playlist(playlist_id, track_id)
	print(res)


def add_playlists(playlists: list[dict]):
	db_playlists.add_playlists(playlists)


def add_liked_tracks(tracks: list[dict]):
	db_tracks.add_tracks(tracks, liked=True)


def add_tracks_to_playlist(playlist_id: str, tracks: list[dict]):
	db_playlists.add_tracks_to_playlist(playlist_id, tracks)


def add_tracks_to_all_playlists():
	playlist_ids = db_playlists.get_playlists()	

	for playlist_id in playlist_ids:
		with open(f'./data/playlists/{playlist_id}.json') as f:
			tracks = json.load(f)

		print(tracks)

	# filenames = glob.glob('./data/playlists/*.json')
	# for f in filenames:
	# 	print(len(tracks))

