import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from logger import log

redirect_uri = 'http://localhost:8080/'
scope = 'playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                               client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def has_playlist_changed(playlist):
	with open('playlists.json') as f:
		playlists_data = json.load(f)

	for playlist_data in playlists_data:
		if playlist_data['name'] == playlist['name']:
			if playlist_data['snapshot_id'] != playlist['snapshot_id']:
				playlist_data['snapshot_id'] = playlist['snapshot_id']
				with open('playlists.json', 'w') as f:
					f.write(json.dumps(playlists_data, indent=2))
				
				return True
			return False

def get_tracks_in_playlist(playlist):

	snapshot_id = playlist['snapshot_id']
	num_tracks_in_playlist = playlist['tracks']['total']

	limit = 50
	offset = num_tracks_in_playlist - 50
	tracks = sp.playlist_items(playlist['id'],
														 fields='items',
														 offset=offset,
														 limit=limit)['items']

	tracks.reverse()
	return tracks


def get_track_ids(tracks):
	return [track['track']['id'] for track in tracks]


def initialize_playlist(playlist_id, tracks):
	track_ids = get_track_ids(tracks)
	sp.playlist_add_items(playlist_id, track_ids)


def update_playlist(playlist_data):
	playlist = sp.playlist(playlist_data['all'])

	if has_playlist_changed(playlist):
		# TODO: display newly added songs in log
		log.info(f"{playlist_data['name']} has changed. Adding new songs")
		most_recent_tracks = get_tracks_in_playlist(playlist)
		track_ids = get_track_ids(most_recent_tracks)
		sp.playlist_replace_items(playlist_data['snippet'], track_ids)
	else:
		log.debug(f"{playlist_data['name']} hasn't changed.")



if __name__ == "__main__":	
	with open('playlists.json') as f:
		playlists = json.load(f)

	for playlist in playlists:
		update_playlist(playlist)


# playlist = sp.playlist('spotify:playlist:6LB26f7o7YcANtlVuxhXZq')
# with open('../requests/playlist.json', 'w') as f:
# 	f.write(json.dumps(playlist, indent=2))