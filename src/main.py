import os
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from logger import log

def get_playlist_data():
	with open('playlists.json') as f:
		return json.load(f)
def set_playlist_data(playlists_data):
	with open('playlists.json', 'w') as f:
		f.write(json.dumps(playlists_data, indent=2))



def find_playlist_in_live_playlists(uri, playlists):
	for playlist in playlists['items']:
		if playlist['uri'] == uri:
			return playlist
	raise Exception('Playlist not found.')

def has_playlist_changed(playlist_data, live_playlist):
	if playlist_data['snapshot_id'] != live_playlist['snapshot_id']:
		playlist_data['snapshot_id'] = live_playlist['snapshot_id']
		return True
	return False

def get_tracks_in_playlist(playlist):

	num_tracks_in_playlist = playlist['tracks']['total']

	limit = 50
	offset = num_tracks_in_playlist - 50
	tracks = sp.playlist_items(playlist['id'],
														 fields='items',
														 offset=offset,
														 limit=limit)['items']

	tracks.reverse()
	return tracks
def update_playlist(playlist_data, live_playlist):
	get_track_ids = lambda tracks: [track['track']['id'] for track in tracks]

	most_recent_tracks = get_tracks_in_playlist(live_playlist)
	track_ids = get_track_ids(most_recent_tracks)
	sp.playlist_replace_items(playlist_data['snippet'], track_ids)

def update_all_playlists():
	playlists = sp.current_user_playlists()
	playlists_data = get_playlist_data()

	for playlist_data in playlists_data:
		live_playlist = find_playlist_in_live_playlists(playlist_data['all'], playlists)

		if has_playlist_changed(playlist_data, live_playlist):
			# TODO: display newly added songs in log
			log.info(f"{playlist_data['name']} has changed. Adding new songs")

			set_playlist_data(playlists_data)
			update_playlist(playlist_data, live_playlist)

		else:
			log.debug(f"{playlist_data['name']} hasn't changed.")


if __name__ == "__main__":
	redirect_uri = 'http://localhost:8080/'
	scope = 'playlist-modify-private playlist-read-private'

	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
																								 client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
																								 redirect_uri=redirect_uri,
																								 scope=scope))

	update_all_playlists()

	# playlists = sp.current_user_playlists()
	# with open('../requests/playlists.json', 'w') as f:
	# 	f.write(json.dumps(playlists, indent=2))