from enum import Enum

import helpers
import settings # pylint: disable=unused-import
from main import sp, all_playlists

from logger import log
# pylint: disable=logging-fstring-interpolation

class PlaylistType(Enum):
	ALL = 'all'
	SNIPPET = 'snippet'
		
def find_playlist_in_live_playlists(uri):
	for playlist in all_playlists['items']:
		if playlist['uri'] == uri:
			return playlist
	raise Exception('Playlist not found.')

def has_playlist_changed(playlist_data, live_playlist):
	if playlist_data['snapshot_id'] != live_playlist['snapshot_id']:
		return True
	return False


def get_tracks_in_playlist(playlist_uri, limit=None, offset=None):
	if offset is not None:
		playlist = find_playlist_in_live_playlists(playlist_uri)
		num_tracks_in_playlist = playlist['tracks']['total']
		offset = num_tracks_in_playlist - offset
		if offset < 0:
			offset = 0

	tracks = sp.playlist_items(playlist_uri,
														 fields='items',
														 limit=limit,
														 offset=offset
														 )['items']
	tracks.reverse()
	return tracks

def update_snippet_playlist(playlist_data):
	get_track_ids = lambda tracks: [track['track']['id'] for track in tracks]

	# limit is the amount of songs I want in the snippet playlist
	most_recent_tracks = get_tracks_in_playlist(playlist_data['all']['uri'], limit=100, offset=100)
	track_ids = get_track_ids(most_recent_tracks)
	sp.playlist_replace_items(playlist_data['snippet']['uri'], track_ids)




def update_all_playlist(playlist_data):
	get_track_ids = lambda tracks: [track['track']['id'] for track in tracks]

	snippet_tracks = get_tracks_in_playlist(playlist_data['snippet']['uri'])
	snippet_track_ids = get_track_ids(snippet_tracks)
	
	all_tracks = get_tracks_in_playlist(playlist_data['all']['uri'])
	all_track_ids = get_track_ids(all_tracks)

	def not_in(a_list):
		def fn(val):
			if val in a_list:
				return False
			return True
		return fn

	new_tracks = list(filter(not_in(all_track_ids), snippet_track_ids))
	removed_tracks = list(filter(not_in(snippet_track_ids), all_track_ids))
	# new_tracks.reverse()
	# removed_tracks.reverse()

	sp.playlist_remove_all_occurrences_of_items(playlist_data['all']['uri'], removed_tracks)
	sp.playlist_add_items(playlist_data['all']['uri'], new_tracks)


	for track_id in new_tracks:
		for t in snippet_tracks:
			if track_id == t['track']['id']:
				log.debug(f"new track: {t['track']['name']}")
				break

	for track_id in removed_tracks:
		for t in all_tracks:
			if track_id == t['track']['id']:
				log.debug(f"removed track: {t['track']['name']}")
				break

	log.debug(f'{new_tracks=}')
	log.debug(f'{removed_tracks=}')




def update_snapshot_of_playlist(playlist, playlists_data, fetch_new=True):
	global all_playlists
	if fetch_new:
		all_playlists = sp.current_user_playlists()

	live_playlist = find_playlist_in_live_playlists(playlist['uri'])
	playlist['snapshot_id'] = live_playlist['snapshot_id']
	helpers.set_playlist_data(playlists_data)


def check_for_changes(playlist_to_check_id: PlaylistType):
	# TODO: refactor, this function is too big
	playlists_data = helpers.get_playlist_data()
	for playlist_data in playlists_data:
		live_playlist = find_playlist_in_live_playlists(playlist_data[playlist_to_check_id.value]['uri'])

		playlist_to_check = playlist_data[playlist_to_check_id.value]
		if has_playlist_changed(playlist_to_check, live_playlist):
			log.info(f"{playlist_data['name']} has changed. Changing playlist.") # TODO: display newly added songs in log

			update_snapshot_of_playlist(playlist_to_check, playlists_data, fetch_new=False)
		
			if playlist_to_check_id == PlaylistType.ALL:
				playlist_to_update = playlist_data[PlaylistType.SNIPPET.value]
				update_snippet_playlist(playlist_data)
			else:
				playlist_to_update = playlist_data[PlaylistType.ALL.value]
				update_all_playlist(playlist_data)

			# TODO: as long as checking snippet playlist for change is not used, the line below is not needed
			# update_snapshot_of_playlist(playlist_to_update, playlists_data)
			
		else:
			log.debug(f"{playlist_data['name']} hasn't changed.")	