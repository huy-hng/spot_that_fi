import os
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ..helpers.helpers import write_dict_to_file
from src.api_handler.tracks import Tracks
from ..helpers.data_types import SpotifyPlaylistType, TracksType

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
		

	def get_one_playlist(self, playlist_id: str) -> SpotifyPlaylistType:
		playlist = self.sp.playlist(playlist_id)
		return SpotifyPlaylistType(**playlist)


	def get_all_playlists(self) -> list[SpotifyPlaylistType]:
		self.api_calls += 1

		all_playlists: list[SpotifyPlaylistType] = []
		offset = 0
		while True:
			playlists: dict = self.sp.current_user_playlists(offset=offset)
			all_playlists += playlists['items']
			if playlists['next'] is None:
				break

			offset += 50

		write_dict_to_file('playlists', all_playlists)

		return all_playlists


	# def get_playlist_tracks(self, playlist_id: str, num_tracks: int):
	# 	tracks = []
	# 	for t in self.get_playlist_tracks_generator(playlist_id):
	# 		if len(tracks) + len(t) > num_tracks:
	# 			rest = num_tracks % 100
	# 			tracks = t[rest:] + tracks
	# 			break
	# 		tracks = t + tracks
	# 	return tracks


	def get_playlist_tracks_generator(self, playlist_id: str):
		""" get latest tracks until num_tracks has been reached or
				no tracks are left """
		items = {'previous': True}
		limit = 100
		tracks_in_playlist: int = self.sp.playlist_items(
																									playlist_id, limit=1)['total']
		offset = tracks_in_playlist - limit
		while items['previous']:
			if offset < 0:
				limit += offset
				offset = 0
				limit = max(1, min(100, limit))

			items: TracksType = self.sp.playlist_items(
																				playlist_id, limit=limit, offset=offset)
			tracks: list[TracksType] = items['items']
			offset -= limit

			yield tracks


	def get_liked_tracks_generator(self):
		items = {'previous': True}
		limit = 50
		liked_tracks_amount = self.sp.current_user_saved_tracks(1)['total']
		offset = liked_tracks_amount - limit
		while items['previous']:
			if offset < 0:
				limit += offset
				offset = 0

			items: TracksType = self.sp.current_user_saved_tracks(limit, offset)
			tracks: list = items['items']
			offset -= limit

			yield tracks


	def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]):
		self.sp.playlist_replace_items(playlist_id, track_ids)


	def remove_tracks(self, uri: str, track_ids: list[str]):
		self.sp.playlist_remove_all_occurrences_of_items(uri, track_ids)


	def add_tracks_at_beginning(self, uri: str, track_ids: list[str]):
		position = 0
		# TEST: how bulk adding behaves, especially if the location is correct
		""" in case isnt, tracks may need to be added one at a time, which 
				could eat at rate limiting """
		self.sp.playlist_add_items(uri, track_ids, position)


	def add_tracks_at_end(self, uri: str,
															track_ids: list[str],
															last_position: int):
		position = last_position

		for track_id in track_ids:
			self.sp.playlist_add_items(uri, [track_id], position)
			position += 1
			time.sleep(0.5)


	def add_tracks_at_end_as_bulk(self,	uri: str,
																			track_ids: list[str],
																			last_position: int):
		self.sp.playlist_add_items(uri, track_ids, last_position)
