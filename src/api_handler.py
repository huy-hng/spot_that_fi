import os
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .helpers import write_dict_to_file
from src.tracks import Tracks
from .data_types import TracksType

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
		

	def get_all_playlists(self):
		self.api_calls += 1

		all_playlists = []
		offset = 0
		while True:
			playlists: dict = self.sp.current_user_playlists(offset=offset)
			all_playlists += playlists['items']
			if playlists['next'] is None:
				break

			offset += 50

		write_dict_to_file('playlists', all_playlists)

		return all_playlists


	def get_latest_tracks(self, uri: str,
															tracks_in_playlist: int,
															num_tracks: int):

		offset = 0
		if num_tracks is not None:
			offset = tracks_in_playlist - num_tracks
			offset = 0 if offset < 0 else offset

		tracks = []

		items = {'next': True}
		while items['next']:
			items: TracksType = self.sp.playlist_items(uri, offset=offset)
			tracks += items['items']
			offset += 100

		tracks.reverse()
		return tracks


	def get_tracks_generator(self, uri: str, tracks_in_playlist: int):
		""" get latest tracks until num_tracks has been reached or
				no tracks are left """
		items = {'previous': True} # TODO check if key is correct
		offset = tracks_in_playlist - 100
		while items['previous']:
			# TEST: what happens if theres no previous and I keep yielding
			items: TracksType = self.sp.playlist_items(uri, offset=offset)
			tracks: list = items['items']
			tracks.reverse()
			offset -= 100

			yield tracks


	def replace_playlist_tracks(self, uri: str, tracks: list[TracksType]):
		track_ids = Tracks.get_ids(tracks)
		self.sp.playlist_replace_items(uri, track_ids)


	def remove_tracks(self, uri: str, tracks: list[TracksType]):
		track_ids = Tracks.get_ids(tracks)
		self.sp.playlist_remove_all_occurrences_of_items(uri, track_ids)


	def add_tracks_at_beginning(self, uri: str, tracks: list[TracksType]):
		track_ids = Tracks.get_ids(tracks)
		position = 0
		# TEST: how bulk adding behaves, especially if the location is correct
		""" in case isnt, tracks may need to be added one at a time, which 
				could eat at rate limiting """
		self.sp.playlist_add_items(uri, track_ids, position)


	def add_tracks_at_end(self, uri: str,
															tracks: list[TracksType],
															last_position: int):
		track_ids = Tracks.get_ids(tracks)
		position = last_position # TEST: off by one error

		for track_id in track_ids:
			self.sp.playlist_add_items(uri, track_id, position)
			position += 1
			time.sleep(0.5) # TEST: if sleep is needed
