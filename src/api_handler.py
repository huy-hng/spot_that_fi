import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .helpers import write_dict_to_file
from .data_types import TracksType

from dotenv import load_dotenv
load_dotenv()

class Spotipy:
	def __init__(self):
		self.api_calls = 0 # TODO: debug why it doesnt increment

		# redirect_uri = 'http://localhost:8080/'
		redirect_uri = 'http://localhost/'
		scope = ''
		scope += 'playlist-read-private '
		scope += 'playlist-modify-private '
		scope += 'playlist-modify-public '
		# scope += 'playlist-read-collaborative'

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


	def get_100_tracks(self, uri, limit=100, offset=0):
		""" limit <= 100 && offset >= 0\n
		if offset is more than there are songs in the playlist,
		it will just fetch 0 songs """

		if limit > 100: limit = 100
		if offset < 0: offset = 0

		self.api_calls += 1

		#TODO check if i can use the prev and next from LivePlaylistsTracksType

		tracks: TracksType = self.sp.playlist_items(
			uri, fields='items', limit=limit, offset=offset)

		write_dict_to_file('tracks', tracks)

		return tracks


	def replace_playlist_tracks(self, uri: str, ids: list[str]):
		self.sp.playlist_replace_items(uri, ids)


	def remove_tracks(self, uri: str, ids: list[str]):
		self.sp.playlist_remove_all_occurrences_of_items(uri, ids)

	def add_tracks_at_beginning(self, uri: str, ids: list[str]):
		self.sp.playlist_add_items(uri, )

sp = Spotipy() # TODO: refactor to __init__.py ?
