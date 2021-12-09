# %%
import json
from src.database import Base, engine
from src.database import db

from src.api_handler import Spotipy

with open('./data/playlists.json') as f:
	playlists = json.loads(f.read())


# %%
def add_tracks_to_playlist():
	db.add_playlists(playlists)

	sp = Spotipy()
	# generator = sp.get_liked_tracks_generator()
	playlist_id = '0oWDXsY9BhT9NKimKwNY9d'
	# sp.
	generator = sp.get_playlist_tracks_generator(playlist_id)
	for batch in generator:
		db.add_tracks_to_playlist(playlist_id, batch)
		break

add_tracks_to_playlist()

# %%