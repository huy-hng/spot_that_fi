# %%
import json
from src.database import Base, engine
from src.database.db import Database

from src.api_handler import Spotipy

with open('./data/playlists.json') as f:
	playlists = json.loads(f.read())

db = Database()

# %%
def add_tracks_to_playlist():
	db.add_playlists(playlists)

	sp = Spotipy()
	# generator = sp.get_liked_tracks_generator()
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	# sp.
	generator = sp.get_playlist_tracks_generator(playlist_id)
	for batch in generator:
		db.add_playlist_tracks(playlist_id, batch)
		break

# add_tracks_to_playlist()

# %%
def check_track_in_playlist():
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	track_id = '14fIlfcmFPlj4V2IazeJ25'
	# track_id = 'asd14fIlfcmFPlj4V2IazeJ25'
	res = db.is_track_in_playlist(playlist_id, track_id)
	print(res)

check_track_in_playlist()