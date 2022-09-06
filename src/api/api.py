import os
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src import types
from src.helpers.exceptions import PlaylistNotFoundError
from src.helpers.logger import log
from src.helpers.helpers import grouper, write_dict_to_file

from dotenv import load_dotenv

load_dotenv()

""" This is a wrapper around the spotipy module
	to give it more convenience features """

redirect_uri = 'http://localhost:8080/'
# redirect_uri = 'http://localhost/'
scope = ''
scope += 'playlist-read-private '
scope += 'playlist-modify-private '
scope += 'playlist-modify-public '
scope += 'playlist-read-collaborative'

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
		client_id=os.getenv('SPOTIPY_CLIENT_ID'),
		client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
		redirect_uri=redirect_uri, scope=scope))


def like_tracks(track_ids: list[str]):
	spotify.current_user_saved_tracks_add(track_ids)


def get_liked_tracks_generator(limit=50):
	""" returns a generator that loops over liked tracks
		in reverse chronological order.
		
		First item in first iteration
		is the most recently liked track. """
	# items: types.tracks.LikedTracksListDict | None
	offset = 0

	while True:
		items = spotify.current_user_saved_tracks(limit, offset)
		if items is None: continue
		items = types.tracks.LikedTracksListDict(items)
		write_dict_to_file('liked_tracks', items)
		offset += limit

		yield items

		if not items.next:
			break


def get_one_playlist(playlist_id: str):
	""" should accept argument as uri, url and id """
	res = spotify.playlist(playlist_id)
	if res is None:
		raise PlaylistNotFoundError(f'Cannot find playlist with ID {playlist_id}')
	return types.playlists.SinglePlaylist(res)


def get_all_playlists():
	""" api call expense: 50 playlists = 1 call \n
			if one has 60 playlists in their spotify,
			this functions would do 2 api calls """


	all_playlists: list[dict] = []
	offset = 0

	while True:
		playlists: dict | None = spotify.current_user_playlists(offset=offset)

		if playlists is None:
			return []

		all_playlists += playlists['items']
		if playlists['next'] is None:
			break

		offset += 50
		# write_dict_to_file('current_user_playlists2', playlists)


	parsed_playlists = [
		types.playlists.AllPlaylists(playlist)
		for playlist in all_playlists
	]

	return parsed_playlists


def _get_playlist_tracks_generator(
	playlist_id: str, total_tracks: int=0, *, limit=100):
	""" Get latest tracks until total_tracks has been reached
		or no tracks are left.

		Args:
			playlist_id: id of playlist to get tracks from
			total_tracks: total_tracks in playlist. Use this to save an api call
			limit: amount of tracks to get at once

		The order is the same as in spotify without any sorting.
		The first returned item is the most recently added tracks
		
		the section that is returned first are the items that have been
		added last
		
		so if my playlist is [0,1,2,3,4] and 0 is the first track 
		that has been added and my limit is 2, then the first yield is
		[3,4], then comes [1,2] and at last [0],
		where the generator terminates

		### Note
		Since on spotify new tracks are by default added to 'the bottom'
		of the playlist it appears that playlists are chronologically
		sorted from first added to last added
	"""

	clamp_limit = lambda limit: max(1, min(100, limit))
	limit = clamp_limit(limit)

	offset = max(0, total_tracks - limit)
	while items := spotify.playlist_items(playlist_id, limit=clamp_limit(limit), offset=offset):
		if items is None: break

		parsed = types.playlists.SinglePlaylistTracks(items)
		if total_tracks != parsed.total: # fixes wrong total_tracks input
			total_tracks = parsed.total
			offset = max(0, total_tracks - limit)
			continue

		offset = parsed.offset
		offset -= limit

		if offset < 0:
			limit += offset
			offset = 0

		yield parsed

		if not parsed.previous:
			break


def _replace_playlist_tracks(playlist_id: str, track_ids: list[str]):
	""" Replaces all tracks in playlist.

		Adding multiple tracks that aren't already in the playlist
		results in wonky order.
		Not sorting the playlist in spotify shows
		the correct order, but when sorted by date added, it is scrambled.
		The reason for that is probably date_added attribute is all the same.
	"""
	spotify.playlist_replace_items(playlist_id, track_ids)


def _add_tracks_to_playlist(
	playlist_id: str, track_ids: list[str], position: int, group_size=1):
	""" Adds tracks to playlist. 

		Args:
			playlist_id:
				the id or uri of the playlist to add tracks to
			track_ids:
				a list of track ids to add to the playlist
			position:
				the position to add the tracks to
				if position == -1: add at the end
			group_size:
				optional argument for batching tracks (to save on rate limiting)
				if group_size <= 0: add all tracks at once
				if group_size == 1: add one track at a time
				if group_size > 1: add {group_size} tracks at once
	"""
	group_size = max(0, group_size)

	if position == -1:
		position = get_one_playlist(playlist_id).tracks.total

	curr_position = position

	groups = grouper(track_ids, group_size)
	for group in groups:
		spotify.playlist_add_items(playlist_id, group, curr_position)
		curr_position += group_size
		time.sleep(0.5)


def _remove_tracks(playlist_id: str, track_ids: list[str]):
	# TEST how does this behave if tracks arent in playlist
	spotify.playlist_remove_all_occurrences_of_items(playlist_id, track_ids)
