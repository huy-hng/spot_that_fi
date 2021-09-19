import math
from typing import Union

from src.tracks import Tracks
from src.data_types import LivePlaylistType
from src.api_handler import sp

class LivePlaylist:
	""" handles crud operations of a live playlist
	the methods shouldnt be complicated
	the bulk logic should be done by the api_handler """
	def __init__(self, playlist: LivePlaylistType):
		self.uri = playlist['uri']
		self.snapshot_id = playlist['snapshot_id']
		self.name = playlist['name']
		self.num_tracks = playlist['tracks']['total']

		self.tracks = Tracks()

	def get_tracks(self, num_songs: int=100):
		raise NotImplementedError()
		offset = 0 # TODO calc offset
		self.tracks.add_tracks(sp.get_tracks(self.uri, num_songs, offset))
		for _ in range(0, num_songs, 100):
			# TODO: debug if the correct amount of steps are taken
			self.tracks.add_tracks(sp.get_100_tracks(self.uri))

		
	def get_latest_tracks(self, num_songs: Union[int, None]=100):

		if num_songs is None:
			num_songs = self.num_tracks

		num_batches = math.ceil(num_songs / 100)
		offset = self.num_tracks - num_songs
		if offset < 0: offset = 0

		if num_songs > self.num_tracks:
			# check if num_songs is not bigger than actual songs in the playlist
			# otherwise it will make unneccesary calls to the api
			num_batches = 1

		tracks = []
		for _ in range(num_batches):
			tracks += sp.get_100_tracks(self.uri, 100, offset)
			offset += 100

		tracks.reverse()
		self.tracks.add_tracks(tracks)
		return self.tracks

class LivePlaylists:
	""" handles loading live playlist data and manages them """
	def __init__(self):
		self.playlists: list[LivePlaylist] = []
		self.names: dict[str, int] = {}
		self.uri: dict[str, int] = {}

		self.update_data()


	def update_data(self):
		playlists: list[LivePlaylistType] = sp.get_all_playlists()

		for index, playlist in zip(range(len(playlists)), playlists):
			self.playlists.append(LivePlaylist(playlist))
			self.names[playlist['name']] = index
			self.uri[playlist['uri']] = index

	def get_by_name(self, name: str):
		index = self.names.get(name)
		if index is None:
			raise Exception('Playlist Name does not exist.')

		return self.playlists[index]


	def get_by_uri(self, uri: str):
		index = self.uri.get(uri)
		if index is None:
			raise Exception('Playlist uri does not exist.')

		return self.playlists[index]
