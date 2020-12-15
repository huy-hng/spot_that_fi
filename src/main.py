import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = '9d91738ece6447399f598fe544696c51'
client_secret = '56838afd9ee448dfbd1770c7fc4a32e6'
redirect_uri = 'http://130.83.4.219:7768/'
redirect_uri = 'http://localhost:8080/'
scope = 'playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))


def get_songs_in_playlist(playlist_id):
	results = sp.playlist_items(playlist_id, limit=1) # FIX: inefficient request that only gets the amount of songs
	num_songs_in_playlist = results['total']

	limit = 50
	offset = num_songs_in_playlist - 50
	results = sp.playlist_items(playlist_id, offset=offset, limit=limit)
	
	sorted_songs: list = results['items']
	sorted_songs.reverse()
	return sorted_songs



def initialize_playlist(playlist_id, songs):
	songs_ids = [song['track']['id'] for song in songs]
	print(songs_ids)
	sp.playlist_add_items(playlist_id, songs_ids)

def update_playlist(playlist_id):
	songs_ids = [song['track']['id'] for song in songs]
	sp.user_playlist_create()



calm_all_uri = 'spotify:playlist:6LB26f7o7YcANtlVuxhXZq'
calm_snippet_uri = 'spotify:playlist:2OBconDUKoGs6BoDTVMVvk'
most_recent_calm_songs = get_songs_in_playlist(calm_all_uri)
initialize_playlist(calm_snippet_uri, most_recent_calm_songs)


with open('../requests/results.json', 'w') as f:
	f.write(json.dumps(most_recent_calm_songs, indent=2))