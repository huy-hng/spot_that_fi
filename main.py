import json
from src.database import db

from src.api_handler import Spotipy

with open('./data/playlists.json') as f:
	playlists = json.loads(f.read())

sp = Spotipy()

def add_tracks_to_playlist():
	db.add_playlists(playlists)

	# generator = sp.get_liked_tracks_generator()
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	# sp.
	generator = sp.get_playlist_tracks_generator(playlist_id)
	for batch in generator:
		db.add_tracks_to_playlist(playlist_id, batch)
		break

# add_tracks_to_playlist()

def add_liked_tracks():
	gen = sp.get_liked_tracks_generator()
	for i, batch in enumerate(gen):
		print(i)
		db.add_tracks(batch)



def liked_songs_in_playlists():
	db.get_liked_tracks_not_in_playlists()

# add_liked_tracks()
liked_songs_in_playlists()