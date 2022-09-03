import os
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src import types
from src.helpers.exceptions import PlaylistNotFoundError
from src.helpers.logger import log
from src.helpers.helpers import write_dict_to_file

from dotenv import load_dotenv

load_dotenv()

class Spotipy:
	""" This is a wrapper around the spotipy module
		to give it more convenience features """
	def __init__(self):
		self.api_calls = 0 # FIX: debug why it doesnt increment

		redirect_uri = 'http://localhost:8080/'
		# redirect_uri = 'http://localhost/'
		scope = ''
		scope += 'playlist-read-private '
		scope += 'playlist-modify-private '
		scope += 'playlist-modify-public '
		scope += 'playlist-read-collaborative'

		self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
				client_id=os.getenv('SPOTIPY_CLIENT_ID'),
				client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
				redirect_uri=redirect_uri, scope=scope))
		

	#region create
	def like_tracks(self, track_ids: list[str]):
		self.sp.current_user_saved_tracks_add(track_ids)
	#endregion


	#region read
	def get_one_playlist(self, playlist_id: str):
		""" should accept argument as uri, url and id """
		playlist: dict = self.sp.playlist(playlist_id)
		# write_dict_to_file('get_one_playlist', playlist)
		return types.playlists.SinglePlaylist(playlist)


	def get_all_playlists(self):
		""" api call expense: 50 playlists = 1 call \n
				if one has 60 playlists in their spotify,
				this functions would do 2 api calls """

		self.api_calls += 1

		all_playlists: list[dict] = []
		offset = 0

		while True:
			playlists: dict | None = self.sp.current_user_playlists(offset=offset)

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

	def _get_playlist_items(self, playlist_id: str, *, limit=100, offset=0):
		items = self.sp.playlist_items(playlist_id, limit=limit, offset=offset)
		if items is None:
			raise PlaylistNotFoundError(
				f'Playlist with ID {playlist_id} could not be found on Spotify')
		return items

	def get_playlist_tracks_generator(
		self, playlist_id: str, total_tracks: int=0, *, limit=100):
		""" get latest tracks until total_tracks has been reached
			or no tracks are left 

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
		# items = {'previous': True}

		# FIX: below api call can be omitted by passing the playlist
			# as AllPlaylists or SinglePlaylist class from types
			# or pass total tracks as param
		if total_tracks == 0:
			items = self.sp.playlist_items(playlist_id)
			if items is None:
				raise PlaylistNotFoundError(
					f'Playlist with ID {playlist_id} could not be found on Spotify')
			total_tracks = items['total']


		offset = total_tracks - limit

		while True:
			if offset < 0:
				limit += offset
				offset = 0
				limit = max(1, min(100, limit))

			items: dict | None = self.sp.playlist_items(
				playlist_id, limit=limit, offset=offset)

			if items is None: continue
			parsed = types.playlists.SinglePlaylistTracks(items)

			offset -= limit
			yield parsed

			if not parsed.previous:
				break


	def get_liked_tracks_generator(self, limit=50):
		""" returns a generator that loops over liked tracks
			in reverse chronological order.
			
			First item in first iteration
			is the most recently liked track. """
		# items: types.tracks.LikedTracksListDict | None
		offset = 0

		while True:
			items = self.sp.current_user_saved_tracks(limit, offset)
			if items is None: continue
			items = types.tracks.LikedTracksListDict(items)
			write_dict_to_file('liked_tracks', items)
			offset += limit

			yield items

			if not items.next:
				break
	#endregion

	#region update
	def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]):
		""" Replaces all tracks in playlist.

			Adding multiple tracks that aren't already in the playlist
			results in wonky order.
			Not sorting the playlist in spotify shows
			the correct order, but when sorted by date added, it is scrambled.
			The reason for that is probably date_added attribute is all the same.
		"""
		self.sp.playlist_replace_items(playlist_id, track_ids)


	def add_tracks_at_beginning(self, uri: str, track_ids: list[str]):
		position = 0
		# TEST: how bulk adding behaves, especially if the location is correct
		""" in case isnt, tracks may need to be added one at a time, which 
				could eat at rate limiting """
		self.sp.playlist_add_items(uri, track_ids, position)


	def add_tracks_at_end(self,
			uri: str, track_ids: list[str], last_position: int):

		position = last_position

		for track_id in track_ids:
			self.sp.playlist_add_items(uri, [track_id], position)
			position += 1
			time.sleep(0.5)


	def add_tracks_at_end_as_bulk(self,
		uri: str,
		track_ids: list[str],
		last_position: int):
		self.sp.playlist_add_items(uri, track_ids, last_position)
	#endregion


	#region delete
	def remove_tracks(self, uri: str, track_ids: list[str]):
		# TEST how does this behave if tracks arent in playlist
		self.sp.playlist_remove_all_occurrences_of_items(uri, track_ids)
	#endregion


	@staticmethod
	def _get_id(id: str):
		""" converts uris and urls to ids and returns it """
		type_ = 'playlist'

		error = False
		itype = None

		fields = id.split(":")
		if len(fields) >= 3:
			itype = fields[-2]
			if type_ != itype:
				error = True
			return fields[-1]

		fields = id.split("/")
		if len(fields) >= 3:
			itype = fields[-2]
			if type_ != itype:
				error = True
			return fields[-1].split("?")[0]

		if error:
			log.warning(f'Expected id of type {type_} but found type {itype}, {id}')
		return id

