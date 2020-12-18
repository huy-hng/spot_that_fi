import os
from enum import Enum

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# pylint: disable=unused-import
# pylint: disable=logging-fstring-interpolation

import helpers
import settings 
from logger import log

class PlaylistType(Enum):
	ALL = 'all'
	SNIPPET = 'snippet'



def find_playlist_in_live_playlists(uri, playlists):
	for playlist in playlists['items']:
		if playlist['uri'] == uri:
			return playlist
	raise Exception('Playlist not found.')

def has_playlist_changed(playlist_data, live_playlist):
	if playlist_data['snapshot_id'] != live_playlist['snapshot_id']:
		return True
	return False

def get_tracks_in_all_playlist(playlist):

	num_tracks_in_playlist = playlist['tracks']['total']

	limit = 50
	offset = num_tracks_in_playlist - 50
	tracks = sp.playlist_items(playlist['id'],
														 fields='items',
														 offset=offset,
														 limit=limit)['items']

	tracks.reverse()
	
	return tracks

def update_snippet_playlist(playlist_data, live_playlist):
	get_track_ids = lambda tracks: [track['track']['id'] for track in tracks]

	most_recent_tracks = get_tracks_in_all_playlist(live_playlist)
	track_ids = get_track_ids(most_recent_tracks)
	sp.playlist_replace_items(playlist_data['uri'], track_ids)


def get_tracks_in_snippet_playlist(playlist):
	tracks = sp.playlist_items(playlist['id'], fields='items')['items']
	tracks.reverse()
	return tracks

def update_all_playlist(playlist_data, live_playlist):
	get_track_ids = lambda tracks: [track['track']['id'] for track in tracks]

	tracks = get_tracks_in_snippet_playlist(live_playlist)
	track_ids = get_track_ids(tracks)

	all_tracks = sp.playlist_items(playlist_data['uri'], fields='items')['items']

	# sp.playlist_replace_items(playlist_data['uri'], track_ids)



def check_for_changes(playlist_to_check_id: PlaylistType, all_playlists):
	# TODO: refactor, this function is too big
	playlists_data = helpers.get_playlist_data()
	for playlist_data in playlists_data:
		live_playlist = find_playlist_in_live_playlists(playlist_data[playlist_to_check_id.value]['uri'], all_playlists)

		playlist_to_check = playlist_data[playlist_to_check_id.value]
		if has_playlist_changed(playlist_to_check, live_playlist):
			log.info(f"{playlist_data['name']} has changed. Adding new songs") # TODO: display newly added songs in log

			playlist_to_check['snapshot_id'] = live_playlist['snapshot_id']
			helpers.set_playlist_data(playlists_data)
		
			if playlist_to_check_id == PlaylistType.ALL:
				playlist_to_update_id = PlaylistType.SNIPPET
				playlist_to_update_fn = update_snippet_playlist
			else:
				playlist_to_update_id = PlaylistType.ALL
				playlist_to_update_fn = update_all_playlist


			playlist_to_update = playlist_data[playlist_to_update_id.value]

			playlist_to_update_fn(playlist_to_update, live_playlist)

			# FIX: refactor this to update snapshot of updated playlist
			live_updated_playlist = find_playlist_in_live_playlists(playlist_to_update['uri'], all_playlists)
			playlist_to_update['snapshot_id'] = live_updated_playlist['snapshot_id']
			helpers.set_playlist_data(playlists_data)
		else:
			log.debug(f"{playlist_data['name']} hasn't changed.")	


def main():
	log.info('')
	all_playlists = sp.current_user_playlists()
	# check_for_changes(PlaylistType.ALL, all_playlists)
	check_for_changes(PlaylistType.SNIPPET, all_playlists)


if __name__ == '__main__':
	redirect_uri = 'http://localhost:8080/'
	scope = 'playlist-modify-private playlist-read-private'

	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                 client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
																							   redirect_uri=redirect_uri, scope=scope))

	main()
