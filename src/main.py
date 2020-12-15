import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

redirect_uri = 'http://localhost:8080/'
scope = 'playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                               client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def get_tracks_in_playlist(playlist_id):
	num_tracks_in_playlist = sp.playlist_items(playlist_id, fields='total')['total']

	limit = 50
	offset = num_tracks_in_playlist - 50
	tracks = sp.playlist_items(playlist_id, fields='items', offset=offset, limit=limit)['items']

	tracks.reverse()
	return tracks


def get_track_ids(tracks):
	return [track['track']['id'] for track in tracks]


def initialize_playlist(playlist_id, tracks):
	track_ids = get_track_ids(tracks)
	sp.playlist_add_items(playlist_id, track_ids)


def update_playlist(playlist):

	most_recent_tracks = get_tracks_in_playlist(playlist['all'])
	track_ids = get_track_ids(most_recent_tracks)
	sp.playlist_replace_items(playlist['snippet'], track_ids)


with open('playlists.json') as f:
	playlists = json.load(f)

for playlist in playlists:
	update_playlist(playlist)

playlist = sp.playlist('spotify:playlist:6LB26f7o7YcANtlVuxhXZq')

with open('../requests/playlist.json', 'w') as f:
	f.write(json.dumps(playlist, indent=2))