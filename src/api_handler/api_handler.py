import os
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src import types
from src.helpers.logger import log
from src.helpers.helpers import write_dict_to_file


from dotenv import load_dotenv
load_dotenv()

class Spotipy:
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
		write_dict_to_file('get_one_playlist', playlist)
		return types.playlists.SinglePlaylist(playlist)


	def get_all_playlists(self):
		""" api call expense: 50 playlists = 1 call \n
				if one has 60 playlists in their spotify,
				this functions would do 2 api calls """

		self.api_calls += 1

		all_playlists: list[dict] = []
		offset = 0

		while True:
			playlists: dict = self.sp.current_user_playlists(offset=offset)
			all_playlists += playlists['items']
			if playlists['next'] is None:
				break

			offset += 50

		# write_dict_to_file('current_user_playlists', all_playlists)

		parsed_playlists = [
			types.playlists.AllPlaylists(playlist)
			for playlist in all_playlists
		]

		return parsed_playlists


	def get_playlist_tracks_generator(self, playlist_id: str):
		""" get latest tracks until num_tracks has been reached or
				no tracks are left """
		items = {'previous': True}
		limit = 100

		tracks_in_playlist: int = self.sp.playlist_items(playlist_id)['total']
		offset = tracks_in_playlist - limit

		while items['previous']:
			if offset < 0:
				limit += offset
				offset = 0
				limit = max(1, min(100, limit))

			items: dict = self.sp.playlist_items(
				playlist_id, limit=limit, offset=offset)

			tracks: list[dict] = items['items']
			offset -= limit

			# write_dict_to_file('playlist_tracks', items)
			yield tracks


	def get_liked_tracks_generator(self):
		items: types.tracks.LikedTracksListDict
		limit = 50
		offset = 0

		while True:
			items = self.sp.current_user_saved_tracks(limit, offset)
			items = types.tracks.LikedTracksListDict(items)
			write_dict_to_file('liked_tracks', items)
			offset += limit

			yield items
			if not items.next:
				# TODO: check if this logic works
				break
	#endregion

	#region update
	def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]):
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

